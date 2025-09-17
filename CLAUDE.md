# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Structure

This is AuraCoach v2, a body recomposition tracking platform built as a full-stack application with a React frontend and Python backend.

### Architecture Overview
- **Frontend**: React + TypeScript + Vite + TailwindCSS (v4)
- **Backend**: Python-based onboarding logic and calculations
- **Purpose**: Data-driven platform for body recomposition tracking with automated TDEE calculations and adaptive target adjustments

### Directory Structure
```
frontend/           # React frontend application
├── src/
│   ├── components/ # UI components (ui/, layout/)
│   ├── hooks/      # Custom React hooks
│   ├── utils/      # Utility functions (cn.ts, constants.ts)
│   └── types/      # TypeScript type definitions
backend/            # Python backend
├── onboarding_magic/ # Core calculation logic
│   ├── types/      # Type definitions (Goal, ActivityLevel, Sex)
│   ├── protein/    # Protein requirement calculations
│   ├── sleep/      # Sleep optimization logic
│   └── activity/   # Activity level and calorie burn calculations
dev_notes/          # Development documentation and best practices
```

## Development Commands

### Frontend (Run from /frontend directory)
```bash
# Development server
npm run dev

# Build for production
npm run build

# Type checking
tsc -b

# Linting
npm run lint

# Preview production build
npm run preview
```

### Backend
Currently using direct Python imports. No package management setup yet - files are imported directly.

## Code Conventions

### React/TypeScript Best Practices
- Use functional components with explicit TypeScript interfaces
- Follow the React.FC pattern with proper typing
- Use React.memo for pure components
- Implement useCallback for event handlers
- Use useMemo for expensive computations

### TailwindCSS Guidelines
- Mobile-first responsive design approach
- Use `clsx` and `tailwind-merge` via the `cn()` utility function for conditional classes
- Custom color scheme with `auracoach-*` prefixes
- Glassmorphic design patterns

### Component Structure
- UI components in `components/ui/` (Button, Input, etc.)
- Layout components in `components/layout/` (Container, Background)
- Export components through index files
- Use proper TypeScript interfaces for props

## Key Technologies
- **Frontend**: React 19, TypeScript, Vite, TailwindCSS v4, React SWC
- **Styling**: TailwindCSS with custom theme and glassmorphic design
- **Development**: ESLint, TypeScript strict mode
- **Build**: Vite with React SWC plugin

## Product Context
AuraCoach enables users to simultaneously lose fat and maintain/build muscle mass through intelligent tracking and automated calculations. The platform integrates with MyFitnessPal and Oura APIs for comprehensive health data tracking.

Core value proposition: "It IS possible to lose fat and build muscle. All you need is a coach to keep you accountable with the math, and to show you exactly what to do next."