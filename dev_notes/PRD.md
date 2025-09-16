# Body Recomposition Tracking Platform - Product Requirements Document
## Version 1.1 - MVP Specification

---

### Product Vision
A data-driven platform that enables users to simultaneously lose fat and maintain/build muscle mass through intelligent tracking, automated TDEE calculations, and adaptive target adjustments based on weekly progress indicators.

### Core Value Proposition
It IS possible to lose fat and build muscle.
All you need is a coach to keep you accountable with the math,
and to show you exactly what to do next.

AuraCoach removes the cognitive load of diet math by automatically calculating and adjusting personalized targets based on real-time biometric data, while providing clear visual feedback on your adherence to evidence-based body recomposition protocols.

### Success Criteria
- Users achieve 0.5-2 lbs/week fat loss while maintaining lean mass
- The app adds more value than friction to existing workflow. As a result:
    - 100% weekly check-in compliance rate (since it's just me for now)
    - 100% user retention at 8 weeks (since it's just me for now)
- Reduction in target adjustment calculation time from 15+ minutes manual to automated

---

## System Architecture Overview

### Data Integration Points
- **MyFitnessPal API**: Daily total calories consumed, daily macronutrients consumed (just protein for now, but extensible to more in the future)
- **Oura API**: Daily sleep hours, TDEE
   - Note: "Total Burn" shown on the Oura app is your estimated TDEE, which starts with an estimated BMR at 4AM each day, using the Schofield equation which uses your age, height, weight, and sex.
   - If you integrate MFP and Oura with Apple Health and log your weight with MFP daily, Oura automatically updates your weight (and your BMR) too. 

    ```python
    async def make_oura_api_request(endpoint: str, access_token: str, params: Dict = None) -> Dict:
    """Make authenticated request to Oura API v2"""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    url = f"https://api.ouraring.com/v2{endpoint}"
    if params:
        url += "?" + urlencode(params)
    
    print(f"🔍 Making request to: {url}")
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 401:
                raise HTTPException(status_code=401, detail="Oura token expired")
            elif response.status == 429:
                raise HTTPException(status_code=429, detail="Oura API rate limit exceeded")
            elif response.status != 200:
                raise HTTPException(status_code=response.status, detail=f"Oura API error: {await response.text()}")
            
            ## DEBUG: Check response parsing
            # response_text = await response.text()
            #print(f"Raw response text: {response_text}")
            
            parsed_json = json.loads(response_text)
            # print(f"Parsed JSON: {parsed_json}")
            
            return parsed_json

    sleep_data = await make_oura_api_request(
        "/usercollection/sleep",
        access_token,
        {"start_date": "2025-09-01", "end_date": "2025-09-14"}
    )
    
    # Example v2/usercollection/sleep response format:
        #  "id": "f2b1c3d4-e5f6-7890-abcd-ef1234567890",
        #  "day": "2025-09-13",
        #  "total_sleep_duration": 28800,  # seconds
        #  "awake_time": 2400,
        #  "rem_sleep_duration": 7200,
        #  "deep_sleep_duration": 10800,
        #  "light_sleep_duration": 10800,
        #  "bedtime_start": "2025-09-12T23:30:00+00:00",
        #  "bedtime_end": "2025-09-13T07:30:00+00:00"
        #  "heart_rate": {...},
        #  "hrv": {...}
        # ...
    # Example /v2/usercollection/daily_activity
    ```
    ```
    sync_oura_daily(median_bedtime_end_past_30_days, median_bedtime_start_past_30_days)
        - Sync once when user typically wakes up, then again every 2 hours until user typically falls asleep. 
        - If the user authenticates or visits a page and last sync was more than 2 hours ago, should fetch new data.
    ```
- **Internal Database**: User profiles, weight trends, calculated targets (future: custom result metrics)

### Calculation Engine Components
1. **TDEE Estimator**: Oura Total Burn
2. **Adaptive Target System**: Weekly recalibration based on weight trend and user feedback to some sanity check questions
3. **Deficit Manager**: Maintains 500-750 calorie deficit with safety bounds
4. **Averaging Engine**: 7-day rolling averages for weight stability

---

## User Flows

### 1. Onboarding Flow
```
START → Email Authentication → Profile Creation → Baseline Metrics → 
API Authorizations → Goal Setting → Initial Targets Display → END
```

**Required Data Collection:**
- Email address (user input)
- MyFitnessPal API credentials
- Oura API credentials
- Age, sex, current weight (all from Oura)
- Goal timeline (optional: event date)

**System Actions:**
- From Oura
  - Set initial TDEE estimate (median from last 30 days)
- Call onboarding_magic/main.py
    - Set first protein target 
    - Set first sleep target
    - Set initial deficit (-500 calories from TDEE)
- Create user record with encrypted API tokens

### 2. Daily Engagement Flow
```
START → Morning Weight Entry → Data Sync → 
Dashboard Update → Compliance Check → END
```

**User Actions:**
- Single weight entry (same time daily ±2 hours)

**System Actions:**
- Pull MyFitnessPal data (last 24 hours)
- Pull Oura data (previous day's complete data)
- Calculate net caloric balance
- Update rolling 7-day averages
- Flag any missing data points

### 3. Weekly Calibration Flow
```
START → Weight Trend Analysis → User Questionnaire → 
TDEE Adjustment → Target Recalculation → 
Progress Report Generation → END
```

**Decision Tree for TDEE Adjustments:**
```
IF weight_change = 0 OR weight_change > 0:
    IF myfitnesspal_complete = NO:
        SKIP adjustment, flag incomplete data week
    ELSE:
        ASK: "Do you feel you've lost fat/gained muscle?"
        IF user_feels_recomp = YES:
            MAINTAIN current TDEE
        ELSE:
            IF weight_same: REDUCE TDEE by 150 cal
            IF weight_up: REDUCE TDEE by 250 cal
ELIF weight_change < -3 lbs/week:
    INCREASE TDEE by 100 cal (prevent muscle loss)
ELIF weight_change between -0.5 to -2 lbs/week:
    MAINTAIN current TDEE (optimal range)
```

### 4. Data Visualization Flow
```
Daily View → Weekly View → Monthly View → Trend Analysis
```

**View Specifications:**
- **Daily**: Single day snapshot with hourly breakdown where available
- **Weekly**: Mon-Sun with daily averages and target lines
- **Monthly**: 30-day rolling window with trend lines and variance bands

---

## Data Models

### User Model
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP,
    last_login TIMESTAMP,
    
    -- Demographics
    age INTEGER,
    sex ENUM('male', 'female'),
    
    -- Goals
    goal_weight_kg DECIMAL(5,2),
    goal_deadline DATE,
    goal_type ENUM('muscle_gain_recomp', 'muscle_retain_recomp', 'maintain'),
    goal_priority ENUM('aggressive', 'moderate', 'sustainable', 'undefined'),
    target_deficit INTEGER,  -- Removed DEFAULT 500
    deficit_type ENUM('calculated', 'moderate', 'sustainable'),
    
    -- API Credentials (encrypted)
    myfitnesspal_token TEXT,
    oura_token TEXT,
    
    -- Calculated Fields
    current_tdee INTEGER,
    current_optimal_deficit INTEGER DEFAULT 500,
    current_optimal_protein_g INTEGER,
    current_optimal_sleep_hours DECIMAL(3,1) DEFAULT 8.0
);
```

### Daily Metrics Model
```sql
CREATE TABLE daily_metrics (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    date DATE NOT NULL,
    
    -- User Input
    weight_kg DECIMAL(5,2),
    weight_time TIMESTAMP,
    
    -- MyFitnessPal Data
    calories_consumed INTEGER,
    protein_g DECIMAL(6,2),
    carbs_g DECIMAL(6,2),
    fat_g DECIMAL(6,2),
    mfp_last_sync TIMESTAMP,
    
    -- Oura Data
    bmr_calories INTEGER,
    activity_calories INTEGER,
    total_burn INTEGER,
    sleep_hours DECIMAL(3,1),
    sleep_score INTEGER,
    readiness_score INTEGER,
    oura_last_sync TIMESTAMP,
    
    -- Calculated Fields
    net_calories INTEGER, -- consumed - total_burn
    deficit_actual INTEGER,
    protein_per_kg DECIMAL(4,2),
    
    UNIQUE(user_id, date)
);
```

### Weekly Summaries Model
```sql
CREATE TABLE weekly_summaries (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    week_start DATE NOT NULL,
    
    -- Averages
    avg_weight_kg DECIMAL(5,2),
    weight_change_kg DECIMAL(4,2),
    avg_deficit INTEGER,
    avg_protein_g DECIMAL(6,2),
    avg_sleep_hours DECIMAL(3,1),
    
    -- Compliance Metrics
    days_weight_logged INTEGER,
    days_mfp_complete INTEGER,
    days_protein_met INTEGER,
    days_sleep_met INTEGER,
    
    -- User Feedback
    subjective_recomp BOOLEAN,
    measurement_waist_cm DECIMAL(5,2),
    measurement_custom JSON,
    
    -- Adjustments Made
    tdee_adjustment INTEGER,
    new_tdee INTEGER,
    adjustment_reason TEXT,
    
    UNIQUE(user_id, week_start)
);
```

### Measurement Templates Model 
```sql
CREATE TABLE measurement_templates (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    measurement_type ENUM('aesthetic', 'strength', 'performance'),
    
    -- Aesthetic Measurements
    measure_waist BOOLEAN DEFAULT false,
    measure_hip BOOLEAN DEFAULT false,
    measure_chest BOOLEAN DEFAULT false,
    measure_arms BOOLEAN DEFAULT false,
    measure_thighs BOOLEAN DEFAULT false,
    
    -- Strength Metrics
    track_bench_max BOOLEAN DEFAULT false,
    track_squat_max BOOLEAN DEFAULT false,
    track_deadlift_max BOOLEAN DEFAULT false,
    
    -- Performance Metrics
    track_rhr BOOLEAN DEFAULT false,
    track_vo2_max BOOLEAN DEFAULT false,
    track_mile_time BOOLEAN DEFAULT false
);
```

---

## API Specifications

### Authentication Endpoints
```
POST /api/auth/request-magic-link
  Body: { email: string }
  Response: { success: boolean, message: string }

GET /api/auth/verify-token
  Query: { token: string }
  Response: { access_token: string, refresh_token: string }
```

### User Data Endpoints
```
POST /api/users/profile
  Request Body: { 
    age: number,
    sex: string,
    goal_weight_kg: number,
    goal_deadline?: date
  }
  Response: { 
    user_id: string, 
    initial_targets: {
      tdee: number,
      deficit: number,
      deficit_type: string,
      net_calories: number,
      protein_g: number,
      timeline_analysis: {
        feasible: boolean | 'challenging',
        message: string,
        weekly_loss_target: number,
        estimated_completion: date
      }
    }
  }

POST /api/users/connect-service
  Request Body: { 
    service: 'myfitnesspal' | 'oura',
    auth_token: string 
  }
  Response: { connected: boolean, initial_sync: object }
```

### Metrics Endpoints
```
POST /api/metrics/weight
  Request Body: { weight_kg: number, timestamp: datetime }
  Response: { 
    recorded: boolean,
    weekly_average: number,
    trend: 'up' | 'down' | 'stable'
  }

GET /api/metrics/dashboard
  Query: { 
    view: 'daily' | 'weekly' | 'monthly',
    date?: date 
  }
  Response: {
    period: object,
    metrics: {
      calories: { target: number, actual: number, series: array },
      protein: { target: number, actual: number, series: array },
      sleep: { target: number, actual: number, series: array },
      weight: { current: number, trend: array }
    },
    compliance_score: number
  }
```

### Weekly Calibration Endpoints
```
POST /api/calibration/weekly-checkin
  Body: {
    mfp_complete: boolean,
    subjective_recomp: boolean,
    measurements?: object
  }
  Response: {
    previous_tdee: number,
    new_tdee: number,
    adjustment: number,
    reason: string,
    new_targets: {
      calories: number,
      protein: number,
      sleep: number
    }
  }

GET /api/calibration/history
  Query: { weeks: number }
  Response: {
    calibrations: array,
    trend_analysis: object
  }
```

### External Service Sync
```
POST /api/sync/trigger
  Body: { service: 'myfitnesspal' | 'oura' | 'all' }
  Response: { 
    synced: boolean,
    last_sync: datetime,
    records_updated: number
  }

GET /api/sync/status
  Response: {
    myfitnesspal: { connected: boolean, last_sync: datetime },
    oura: { connected: boolean, last_sync: datetime }
  }
```

---

## User Interface Specifications

### Design System Requirements

**Visual Hierarchy:**
- Primary focus on three core metrics: Net Calories, Protein, Sleep
- Target lines as dotted horizontal references
- Color coding: Green (on target ±10%), Yellow (±20%), Red (>20% deviation)
- Weekly view as default landing

**Dashboard Layout:**
```
┌─────────────────────────────────────┐
│  Week of [Date]     [Daily|Weekly*|Monthly]  │
├─────────────────────────────────────┤
│  Body Composition Changes           │
│  ┌─────────────────────────────┐    │
│  │  BF%: 18.7% → 18.3%  (-0.4%) │    │
│  │  SMM: 28.5kg → 28.6kg (+0.1kg)│   │
│  │  Weight: 70kg → 69.2kg (-0.8kg)│  │
│  └─────────────────────────────┘    │
│  Quality Score: 92% (Excellent)     │
├─────────────────────────────────────┤
│  Net Calories (Adjusted for BF%)    │
│  ┌─────────────────────────────┐    │
│  │  [Bar Chart with Dynamic Target]│ │
│  └─────────────────────────────┘    │
│  Target: -420 | Actual Avg: -395    │
│  Max Safe: -520 (based on 18.7% BF) │
├─────────────────────────────────────┤
│  Protein Intake (per kg lean mass)  │
│  ┌─────────────────────────────┐    │
│  │  [Bar Chart with Target Line]│    │
│  └─────────────────────────────┘    │
│  Target: 2.2g/kg | Actual: 2.1g/kg  │
│  Total: 125g target | 119g actual   │
├─────────────────────────────────────┤
│  Sleep & Recovery                   │
│  ┌─────────────────────────────┐    │
│  │  [Bar Chart with Target Zone]│    │
│  └─────────────────────────────┘    │
│  Target: 8h | Actual Avg: 7.5h      │
├─────────────────────────────────────┤
│  ⚠️ Lean Alert: Your BF% requires   │
│  conservative deficits. Max: -520cal │
└─────────────────────────────────────┘
```

### Responsive Breakpoints
- Mobile: Single column, swipeable charts
- Tablet: Two column grid
- Desktop: Three charts visible simultaneously

### Interaction Patterns
- Pull-to-refresh for manual sync
- Tap chart for detailed view
- Long press for historical comparison
- Swipe between time periods

---

## Technical Implementation Considerations

### Performance Requirements
- Dashboard load time < 2 seconds
- API sync completion < 5 seconds per service
- Weekly calculation processing < 1 second

### Data Sync Strategy
```
Sync Priority:
1. Current day weight (immediate)
2. Previous day Oura data (on dashboard load)
3. MyFitnessPal current day (every 4 hours)
4. Historical backfill (background, low priority)
```

### Error Handling
- Graceful degradation when external APIs unavailable
- Local caching of last 7 days data
- Manual entry fallback for all external data points
- Clear user messaging for sync failures

### Security Requirements
- OAuth 2.0 for external service authentication
- Token encryption at rest
- API rate limiting (100 requests/minute per user)
- PII data encryption in database

---

## Migration Path to Full Product

### Phase 1 (MVP - Weeks 1-4)
- Basic authentication and user profiles
- Weight tracking and averaging
- MyFitnessPal integration
- Simple dashboard with calorie tracking

### Phase 2 (Weeks 5-8)
- Oura integration
- Automated TDEE calculations
- Weekly calibration system
- Protein and sleep tracking

### Phase 3 (Weeks 9-12)
- Custom measurement tracking
- Advanced analytics and predictions
- Social features (optional)
- Coach messaging system

### Phase 4 (Post-MVP)
- Machine learning for TDEE prediction
- Photo progress tracking
- Workout plan integration
- Meal planning suggestions

---

## Monitoring and Analytics

### Key Performance Indicators
- Daily Active Users (DAU)
- Weekly weight entry rate
- Average weekly weight change
- TDEE adjustment frequency
- User retention by week

### Event Tracking
```javascript
track_events = {
  'user_signup': { method: 'email' | 'oauth' },
  'weight_entered': { time_of_day: hour, day_of_week: day },
  'dashboard_viewed': { view_type: 'daily' | 'weekly' | 'monthly' },
  'sync_triggered': { service: string, success: boolean },
  'weekly_checkin_completed': { weight_change: number, tdee_adjusted: boolean },
  'target_achieved': { metric: 'calories' | 'protein' | 'sleep' }
}
```

---

## Appendix: TDEE Calculation Methodology

### Base Formula
```
TDEE = BMR + Activity Calories + TEF

Where:
- BMR from Oura (using their proprietary algorithm)
- Activity Calories from Oura (exercise, not so much NEAT)
- TEF = 0.1 × Calories Consumed (Thermic Effect of Food)
```

### Adjustment Algorithm
```python
def get_tdee_adjustment(weight_change, user_feedback):
    if weight_change > 0:
        if user_feedback.feels_recomp:
            return 0  # Maintain
        else:
            return -250  # Reduce
    elif weight_change == 0:
        if user_feedback.feels_recomp:
            return 0  # Maintain
        else:
            return -150  # Slight reduction
    elif weight_change < -3:
        return +100  # Too aggressive
    else:
        return 0  # Optimal range
```

### Safety Bounds
- Minimum net calories: 1200 (women) / 1500 (men)
- Maximum deficit: 1000 calories/day
- Minimum protein: 0.7g/lb body weight
- Maximum weekly adjustment: ±300 calories