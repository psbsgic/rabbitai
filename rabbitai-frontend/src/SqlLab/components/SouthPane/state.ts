
import { connect } from 'react-redux';
import { bindActionCreators, Dispatch } from 'redux';
import * as Actions from '../../actions/sqlLab';
import SouthPane from './SouthPane';

function mapStateToProps({ sqlLab }: Record<string, any>) {
  return {
    activeSouthPaneTab: sqlLab.activeSouthPaneTab,
    databases: sqlLab.databases,
    offline: sqlLab.offline,
    user: sqlLab.user,
  };
}

function mapDispatchToProps(dispatch: Dispatch) {
  return {
    actions: bindActionCreators<any, any>(Actions, dispatch),
  };
}

export default connect<any>(mapStateToProps, mapDispatchToProps)(SouthPane);
