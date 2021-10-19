/* eslint-disable no-unused-expressions */
import { defaultState } from 'src/explore/store';
import exploreReducer from 'src/explore/reducers/exploreReducer';
import * as actions from 'src/explore/actions/exploreActions';

describe('reducers', () => {
  it('sets correct control value given an arbitrary key and value', () => {
    const newState = exploreReducer(
      defaultState,
      actions.setControlValue('NEW_FIELD', 'x', []),
    );
    expect(newState.controls.NEW_FIELD.value).toBe('x');
    expect(newState.form_data.NEW_FIELD).toBe('x');
  });
  it('setControlValue works as expected with a checkbox', () => {
    const newState = exploreReducer(
      defaultState,
      actions.setControlValue('show_legend', true, []),
    );
    expect(newState.controls.show_legend.value).toBe(true);
    expect(newState.form_data.show_legend).toBe(true);
  });
});
