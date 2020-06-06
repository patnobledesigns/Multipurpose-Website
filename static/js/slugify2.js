const titleInput = document.querySelector('input[name=title]');
const slugInput2 = document.querySelector('input[name=slug]');

const slugify2 = (val) =>{
    return val.toString().toLowerCase().trim()
    .replace(/&/g, '-and-')
    .replace(/[\s\W-]+/g, '-')
};

titleInput.addEventListener('keyup', (e) =>{
    slugInput2.setAttribute('value', slugify2(titleInput.value));
});

