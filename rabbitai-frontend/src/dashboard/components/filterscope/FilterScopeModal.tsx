import React, { RefObject } from 'react';
import { styled } from '@superset-ui/core';
import ModalTrigger from 'src/components/ModalTrigger';
import FilterScope from 'src/dashboard/containers/FilterScope';

type FilterScopeModalProps = {
  triggerNode: JSX.Element;
};

const FilterScopeModalBody = styled.div(({ theme: { gridUnit } }) => ({
  padding: gridUnit * 2,
  paddingBottom: gridUnit * 3,
}));

export default class FilterScopeModal extends React.PureComponent<
  FilterScopeModalProps,
  {}
> {
  modal: RefObject<ModalTrigger>;

  constructor(props: FilterScopeModalProps) {
    super(props);

    this.modal = React.createRef();
    this.handleCloseModal = this.handleCloseModal.bind(this);
  }

  handleCloseModal(): void {
    if (this.modal.current) {
      this.modal.current.close();
    }
  }

  render() {
    const filterScopeProps = {
      onCloseModal: this.handleCloseModal,
    };

    return (
      <ModalTrigger
        ref={this.modal}
        triggerNode={this.props.triggerNode}
        modalBody={
          <FilterScopeModalBody>
            <FilterScope {...filterScopeProps} />
          </FilterScopeModalBody>
        }
        width="80%"
      />
    );
  }
}
