
import React from 'react';

const NUM_COLUMNS = 12;

type Control = React.ReactElement | null;

export default function ControlRow({ controls }: { controls: Control[] }) {
  // ColorMapControl renders null and should not be counted
  // in the columns number
  const countableControls = controls.filter(
    control => !['ColorMapControl'].includes(control?.props.type),
  );
  const colSize = NUM_COLUMNS / countableControls.length;
  return (
    <div className="row space-1">
      {controls.map((control, i) => (
        <div className={`col-lg-${colSize} col-xs-12`} key={i}>
          {control}
        </div>
      ))}
    </div>
  );
}
