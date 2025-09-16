import { useState, useCallback } from 'react';

interface UseFocusBlurReturn {
  isFocused: boolean;
  focusProps: {
    onFocus: () => void;
    onBlur: () => void;
  };
}

export const useFocusBlur = (): UseFocusBlurReturn => {
  const [isFocused, setIsFocused] = useState(false);

  const handleFocus = useCallback(() => {
    setIsFocused(true);
  }, []);

  const handleBlur = useCallback(() => {
    setIsFocused(false);
  }, []);

  return {
    isFocused,
    focusProps: {
      onFocus: handleFocus,
      onBlur: handleBlur,
    },
  };
};