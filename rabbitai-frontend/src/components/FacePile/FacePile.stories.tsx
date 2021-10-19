import React from 'react';
import { withKnobs, number } from '@storybook/addon-knobs';
import FacePile from '.';

export default {
  title: 'FacePile',
  component: FacePile,
  decorators: [withKnobs],
};

const firstNames = [
  'James',
  'Mary',
  'John',
  'Patricia',
  'Mohamed',
  'Venkat',
  'Lao',
  'Robert',
  'Jennifer',
  'Michael',
  'Linda',
];
const lastNames = [
  'Smith',
  'Johnson',
  'Williams',
  'Saeed',
  'Jones',
  'Brown',
  'Tzu',
];

const users = [...new Array(10)].map((_, i) => ({
  first_name: firstNames[Math.floor(Math.random() * firstNames.length)],
  last_name: lastNames[Math.floor(Math.random() * lastNames.length)],
  id: i,
}));

export const SupersetFacePile = () => (
  <FacePile users={users} maxCount={number('maxCount', 4)} />
);
