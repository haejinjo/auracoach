

Mobile-first responsive class combo example:
```typescript
className="w-80 md:w-96 lg:w-[320px]"
```

Use `clsx` and `tailwind-merge` for conditional classes and automerge:
```typescript
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: (string | undefined | null | boolean)[]) {
  return twMerge(clsx(inputs));
}

// Usage
className={cn(
  'glassmorphic rounded-full',
  focused && 'border-fey-accent/30 bg-white/[0.08]',
  error && 'border-red-500/50'
)}
```