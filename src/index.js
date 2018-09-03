function component() {
  let element = document.createElement('div');

  element.innerHTML = ['Hello', 'webszzzzzzssspack'].join(' ');

  return element;
}

document.body.appendChild(component());