
import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import userEvent from '@testing-library/user-event';
import { MainNav as Menu } from 'src/common/components';
import LanguagePicker from './LanguagePicker';

const mockedProps = {
  locale: 'en',
  languages: {
    en: {
      flag: 'us',
      name: 'English',
      url: '/lang/en',
    },
    it: {
      flag: 'it',
      name: 'Italian',
      url: '/lang/it',
    },
  },
};

test('should render', () => {
  const { container } = render(
    <Menu>
      <LanguagePicker {...mockedProps} />
    </Menu>,
  );
  expect(container).toBeInTheDocument();
});

test('should render the language picker', () => {
  render(
    <Menu>
      <LanguagePicker {...mockedProps} />
    </Menu>,
  );
  expect(screen.getByLabelText('Languages')).toBeInTheDocument();
});

test('should render the items', async () => {
  render(
    <Menu>
      <LanguagePicker {...mockedProps} />
    </Menu>,
  );
  userEvent.hover(screen.getByRole('button'));
  expect(await screen.findByText('English')).toBeInTheDocument();
  expect(await screen.findByText('Italian')).toBeInTheDocument();
});
