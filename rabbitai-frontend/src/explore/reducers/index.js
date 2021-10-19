import { combineReducers } from 'redux';

import reports from 'src/reports/reducers/reports';
import charts from '../../chart/chartReducer';
import saveModal from './saveModalReducer';
import explore from './exploreReducer';
import dataMask from '../../dataMask/reducer';
import messageToasts from '../../messageToasts/reducers';

const impressionId = (state = '') => state;

export default combineReducers({
  charts,
  saveModal,
  dataMask,
  explore,
  impressionId,
  messageToasts,
  reports,
});
