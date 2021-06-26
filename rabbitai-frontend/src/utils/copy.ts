const copyTextToClipboard = async (text: string) =>
  new Promise<void>((resolve, reject) => {
    const selection: Selection | null = document.getSelection();
    if (selection) {
      selection.removeAllRanges();
      const range = document.createRange();
      const span = document.createElement('span');
      span.textContent = text;
      span.style.position = 'fixed';
      span.style.top = '0';
      span.style.clip = 'rect(0, 0, 0, 0)';
      span.style.whiteSpace = 'pre';

      document.body.appendChild(span);
      range.selectNode(span);
      selection.addRange(range);

      try {
        if (!document.execCommand('copy')) {
          reject();
        }
      } catch (err) {
        reject();
      }

      document.body.removeChild(span);
      if (selection.removeRange) {
        selection.removeRange(range);
      } else {
        selection.removeAllRanges();
      }
    }

    resolve();
  });

export default copyTextToClipboard;
