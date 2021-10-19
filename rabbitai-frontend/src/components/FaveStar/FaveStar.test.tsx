import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import userEvent from '@testing-library/user-event';
import FaveStar from '.';

jest.mock('src/components/Tooltip', () => ({
  Tooltip: (props: any) => <div data-test="tooltip" {...props} />,
}));

test('render right content', () => {
  const props = {
    itemId: 3,
    saveFaveStar: jest.fn(),
  };

  const { rerender } = render(<FaveStar {...props} isStarred />);
  expect(screen.getByRole('button')).toBeInTheDocument();
  expect(
    screen.getByRole('img', { name: 'favorite-selected' }),
  ).toBeInTheDocument();

  expect(props.saveFaveStar).toBeCalledTimes(0);
  userEvent.click(screen.getByRole('button'));
  expect(props.saveFaveStar).toBeCalledTimes(1);
  expect(props.saveFaveStar).toBeCalledWith(props.itemId, true);

  rerender(<FaveStar {...props} />);
  expect(
    screen.getByRole('img', { name: 'favorite-unselected' }),
  ).toBeInTheDocument();

  expect(props.saveFaveStar).toBeCalledTimes(1);
  userEvent.click(screen.getByRole('button'));
  expect(props.saveFaveStar).toBeCalledTimes(2);
  expect(props.saveFaveStar).toBeCalledWith(props.itemId, false);
});

test('render content on tooltip', () => {
  const props = {
    itemId: 3,
    showTooltip: true,
    saveFaveStar: jest.fn(),
  };

  render(<FaveStar {...props} />);

  expect(screen.getByTestId('tooltip')).toBeInTheDocument();
  expect(screen.getByTestId('tooltip')).toHaveAttribute(
    'id',
    'fave-unfave-tooltip',
  );
  expect(screen.getByTestId('tooltip')).toHaveAttribute(
    'title',
    'Click to favorite/unfavorite',
  );
  expect(screen.getByRole('button')).toBeInTheDocument();
});

test('Call fetchFaveStar only on the first render', () => {
  const props = {
    itemId: 3,
    fetchFaveStar: jest.fn(),
    saveFaveStar: jest.fn(),
    isStarred: false,
    showTooltip: false,
  };

  const { rerender } = render(<FaveStar {...props} />);
  expect(props.fetchFaveStar).toBeCalledTimes(1);
  expect(props.fetchFaveStar).toBeCalledWith(props.itemId);

  rerender(<FaveStar {...{ ...props, itemId: 2 }} />);
  expect(props.fetchFaveStar).toBeCalledTimes(1);
});
