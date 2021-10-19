import React from 'react';
import Popover from 'src/components/Popover';
import { OptionSortType } from 'src/explore/types';
import AdhocFilterEditPopover from 'src/explore/components/controls/FilterControl/AdhocFilterEditPopover';
import AdhocFilter from 'src/explore/components/controls/FilterControl/AdhocFilter';
import { ExplorePopoverContent } from 'src/explore/components/ExploreContentPopover';

interface AdhocFilterPopoverTriggerProps {
  adhocFilter: AdhocFilter;
  options: OptionSortType[];
  datasource: Record<string, any>;
  onFilterEdit: (editedFilter: AdhocFilter) => void;
  partitionColumn?: string;
  createNew?: boolean;
  isControlledComponent?: boolean;
  visible?: boolean;
  togglePopover?: (visible: boolean) => void;
  closePopover?: () => void;
}

interface AdhocFilterPopoverTriggerState {
  popoverVisible: boolean;
}

class AdhocFilterPopoverTrigger extends React.PureComponent<
  AdhocFilterPopoverTriggerProps,
  AdhocFilterPopoverTriggerState
> {
  constructor(props: AdhocFilterPopoverTriggerProps) {
    super(props);
    this.onPopoverResize = this.onPopoverResize.bind(this);
    this.closePopover = this.closePopover.bind(this);
    this.togglePopover = this.togglePopover.bind(this);
    this.state = {
      popoverVisible: false,
    };
  }

  onPopoverResize() {
    this.forceUpdate();
  }

  closePopover() {
    this.togglePopover(false);
  }

  togglePopover(visible: boolean) {
    this.setState({
      popoverVisible: visible,
    });
  }

  render() {
    const { adhocFilter, isControlledComponent } = this.props;

    const { visible, togglePopover, closePopover } = isControlledComponent
      ? {
          visible: this.props.visible,
          togglePopover: this.props.togglePopover,
          closePopover: this.props.closePopover,
        }
      : {
          visible: this.state.popoverVisible,
          togglePopover: this.togglePopover,
          closePopover: this.closePopover,
        };
    const overlayContent = (
      <ExplorePopoverContent>
        <AdhocFilterEditPopover
          adhocFilter={adhocFilter}
          options={this.props.options}
          datasource={this.props.datasource}
          partitionColumn={this.props.partitionColumn}
          onResize={this.onPopoverResize}
          onClose={closePopover}
          onChange={this.props.onFilterEdit}
        />
      </ExplorePopoverContent>
    );

    return (
      <Popover
        placement="right"
        trigger="click"
        content={overlayContent}
        defaultVisible={visible}
        visible={visible}
        onVisibleChange={togglePopover}
        destroyTooltipOnHide={this.props.createNew}
      >
        {this.props.children}
      </Popover>
    );
  }
}

export default AdhocFilterPopoverTrigger;
