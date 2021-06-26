
import React from 'react';

import { QueryState } from '../types';

interface TabStatusIconProps {
  tabState: QueryState;
}

export default function TabStatusIcon({ tabState }: TabStatusIconProps) {
  return <div className={`circle ${tabState}`} />;
}
