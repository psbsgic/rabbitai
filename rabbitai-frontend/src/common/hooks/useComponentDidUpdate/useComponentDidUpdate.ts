import { EffectCallback, useEffect, useRef } from 'react';

export const useComponentDidUpdate = (effect: EffectCallback) => {
  const isMountedRef = useRef(false);
  useEffect(() => {
    if (isMountedRef.current) {
      effect();
    } else {
      isMountedRef.current = true;
    }
  }, [effect]);
};
