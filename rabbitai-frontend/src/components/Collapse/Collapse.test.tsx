
import React from 'react';
import { render, screen } from 'spec/helpers/testing-library';
import userEvent from '@testing-library/user-event';
import { rabbitaiTheme } from '@rabbitai-ui/core';
import { hexToRgb } from 'src/utils/colorUtils';
import Collapse, { CollapseProps } from '.';

function renderCollapse(props?: CollapseProps) {
  return render(
    <Collapse {...props}>
      <Collapse.Panel header="Header 1" key="1">
        Content 1
      </Collapse.Panel>
      <Collapse.Panel header="Header 2" key="2">
        Content 2
      </Collapse.Panel>
    </Collapse>,
  );
}

test('renders collapsed with default props', () => {
  renderCollapse();

  const headers = screen.getAllByRole('button');

  expect(headers[0]).toHaveTextContent('Header 1');
  expect(headers[1]).toHaveTextContent('Header 2');
  expect(screen.queryByText('Content 1')).not.toBeInTheDocument();
  expect(screen.queryByText('Content 2')).not.toBeInTheDocument();
});

test('renders with one item expanded by default', () => {
  renderCollapse({ defaultActiveKey: ['1'] });

  const headers = screen.getAllByRole('button');

  expect(headers[0]).toHaveTextContent('Header 1');
  expect(headers[1]).toHaveTextContent('Header 2');
  expect(screen.getByText('Content 1')).toBeInTheDocument();
  expect(screen.queryByText('Content 2')).not.toBeInTheDocument();
});

test('expands on click', () => {
  renderCollapse();

  expect(screen.queryByText('Content 1')).not.toBeInTheDocument();
  expect(screen.queryByText('Content 2')).not.toBeInTheDocument();

  userEvent.click(screen.getAllByRole('button')[0]);

  expect(screen.getByText('Content 1')).toBeInTheDocument();
  expect(screen.queryByText('Content 2')).not.toBeInTheDocument();
});

test('collapses on click', () => {
  renderCollapse({ defaultActiveKey: ['1'] });

  expect(screen.getByText('Content 1')).toBeInTheDocument();
  expect(screen.queryByText('Content 2')).not.toBeInTheDocument();

  userEvent.click(screen.getAllByRole('button')[0]);

  expect(screen.getByText('Content 1').parentNode).toHaveClass(
    'ant-collapse-content-hidden',
  );
  expect(screen.queryByText('Content 2')).not.toBeInTheDocument();
});

test('renders with custom properties', () => {
  renderCollapse({
    light: true,
    bigger: true,
    bold: true,
    animateArrows: true,
  });

  const header = document.getElementsByClassName('ant-collapse-header')[0];
  const arrow = document.getElementsByClassName('ant-collapse-arrow')[0]
    .children[0];

  const headerStyle = window.getComputedStyle(header);
  const arrowStyle = window.getComputedStyle(arrow);

  expect(headerStyle.fontWeight).toBe(
    rabbitaiTheme.typography.weights.bold.toString(),
  );
  expect(headerStyle.fontSize).toBe(`${rabbitaiTheme.gridUnit * 4}px`);
  expect(headerStyle.color).toBe(
    hexToRgb(rabbitaiTheme.colors.grayscale.light4),
  );
  expect(arrowStyle.transition).toBe('transform 0.24s');
});
