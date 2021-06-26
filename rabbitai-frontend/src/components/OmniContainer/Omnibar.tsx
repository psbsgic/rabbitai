

import React from 'react';
import OmnibarDeprecated from 'omnibar';

interface Props {
  id: string;
  placeholder: string;
  extensions: ((query: string) => Promise<any>)[];
}

/**
 * @deprecated Component "omnibar" does not support prop className or id (the original implementation used className). However, the original javascript code was sending these prop and was working correctly. lol
 * As this behavior is unpredictable, and does not works whitch types, I have isolated this component so that in the future a better solution can be found and implemented.
 * We need to find a substitute for this component or some way of working around this problem
 */
export function Omnibar({ extensions, placeholder, id }: Props) {
  return (
    <OmnibarDeprecated
      // @ts-ignore
      id={id}
      placeholder={placeholder}
      extensions={extensions}
      // autoFocus // I tried to use this prop (autoFocus) but it only works the first time that Omnibar is shown
    />
  );
}
