
import React from 'react';
import SyntaxHighlighter from 'react-syntax-highlighter/dist/cjs/light';
import sql from 'react-syntax-highlighter/dist/cjs/languages/hljs/sql';
import github from 'react-syntax-highlighter/dist/cjs/styles/hljs/github';
import { t } from '@rabbitai-ui/core';

import ModalTrigger from '../../components/ModalTrigger';

SyntaxHighlighter.registerLanguage('sql', sql);

interface HighlightedSqlProps {
  sql: string;
  rawSql?: string;
  maxWidth?: number;
  maxLines?: number;
  shrink?: any;
}

interface HighlightedSqlModalTypes {
  rawSql?: string;
  sql: string;
}

interface TriggerNodeProps {
  shrink: boolean;
  sql: string;
  maxLines: number;
  maxWidth: number;
}

const shrinkSql = (sql: string, maxLines: number, maxWidth: number) => {
  const ssql = sql || '';
  let lines = ssql.split('\n');
  if (lines.length >= maxLines) {
    lines = lines.slice(0, maxLines);
    lines.push('{...}');
  }
  return lines
    .map(line => {
      if (line.length > maxWidth) {
        return `${line.slice(0, maxWidth)}{...}`;
      }
      return line;
    })
    .join('\n');
};

function TriggerNode({ shrink, sql, maxLines, maxWidth }: TriggerNodeProps) {
  return (
    <SyntaxHighlighter language="sql" style={github}>
      {shrink ? shrinkSql(sql, maxLines, maxWidth) : sql}
    </SyntaxHighlighter>
  );
}

function HighlightSqlModal({ rawSql, sql }: HighlightedSqlModalTypes) {
  return (
    <div>
      <h4>{t('Source SQL')}</h4>
      <SyntaxHighlighter language="sql" style={github}>
        {sql}
      </SyntaxHighlighter>
      {rawSql && rawSql !== sql && (
        <div>
          <h4>{t('Raw SQL')}</h4>
          <SyntaxHighlighter language="sql" style={github}>
            {rawSql}
          </SyntaxHighlighter>
        </div>
      )}
    </div>
  );
}

function HighlightedSql({
  sql,
  rawSql,
  maxWidth = 50,
  maxLines = 5,
  shrink = false,
}: HighlightedSqlProps) {
  return (
    <ModalTrigger
      modalTitle={t('SQL')}
      modalBody={<HighlightSqlModal rawSql={rawSql} sql={sql} />}
      triggerNode={
        <TriggerNode
          shrink={shrink}
          sql={sql}
          maxLines={maxLines}
          maxWidth={maxWidth}
        />
      }
    />
  );
}

export default HighlightedSql;
