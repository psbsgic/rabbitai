import React from 'react';

interface IssueCodeProps {
  code: number;
  message: string;
}

export default function IssueCode({ code, message }: IssueCodeProps) {
  return (
    <>
      {message}{' '}
      <a
        href={`https://rabbitai.apache.org/docs/miscellaneous/issue-codes#issue-${code}`}
        rel="noopener noreferrer"
        target="_blank"
      >
        <i className="fa fa-external-link" />
      </a>
    </>
  );
}
