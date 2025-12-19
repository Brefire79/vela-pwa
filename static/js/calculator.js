(function(){
  const display = document.getElementById('display');
  const keys = document.querySelector('.keys');
  let buffer = '';
  let operator = null;
  let operand = null;

  const setDisplay = (val) => { display.value = String(val); };
  const clear = () => { buffer = ''; operator = null; operand = null; setDisplay(0); };
  const back = () => { buffer = buffer.slice(0, -1); setDisplay(buffer || 0); };

  const compute = () => {
    if (operator === null || operand === null || buffer === '') return;
    const a = parseFloat(operand);
    const b = parseFloat(buffer);
    let res = 0;
    switch(operator){
      case '+': res = a + b; break;
      case '-': res = a - b; break;
      case '*': res = a * b; break;
      case '/': res = b === 0 ? 'Erro' : a / b; break;
    }
    buffer = '';
    operator = null;
    operand = res;
    setDisplay(res);
  };

  keys.addEventListener('click', (e) => {
    const t = e.target;
    if (t.tagName !== 'BUTTON') return;
    const action = t.dataset.action;
    const val = t.textContent.trim();

    if (!action) {
      // number or dot
      if (val === '.' && buffer.includes('.')) return;
      buffer += val;
      setDisplay(buffer);
      return;
    }

    switch(action){
      case 'clear': clear(); break;
      case 'back': back(); break;
      case 'add':
      case 'subtract':
      case 'multiply':
      case 'divide': {
        if (buffer === '' && operand == null) return;
        if (operand == null) {
          operand = parseFloat(buffer);
          buffer = '';
        } else if (buffer !== '') {
          compute();
        }
        operator = ({ add: '+', subtract: '-', multiply: '*', divide: '/' })[action];
        break;
      }
      case 'equal': compute(); break;
    }
  });

  // init
  clear();
})();
