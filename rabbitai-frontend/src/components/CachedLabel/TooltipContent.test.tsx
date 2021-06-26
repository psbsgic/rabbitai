

import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import moment from 'moment';
import { TooltipContent } from './TooltipContent';

test('Rendering TooltipContent correctly - no timestep', () => {
  render(<TooltipContent />);
  expect(screen.getByTestId('tooltip-content')?.textContent).toBe(
    'Loaded from cache. Click to force-refresh',
  );
});

test('Rendering TooltipContent correctly - with timestep', () => {
  render(<TooltipContent cachedTimestamp="01-01-2000" />);
  expect(screen.getByTestId('tooltip-content')?.textContent).toBe(
    `Loaded data cached ${moment
      .utc('01-01-2000')
      .fromNow()}. Click to force-refresh`,
  );
});
