const cedula = document.querySelector('#cedula_cliente');
const Name = document.querySelector('#nombre_cliente');
const apellido = document.querySelector('#apellido_cliente');
const telef = document.querySelector('#telefono_cliente');
const email = document.querySelector('#email_cliente');
const password = document.querySelector('#contrasena_cliente');
const match = document.querySelector('#confirmar_contrasena');
const formBtn = document.querySelector('#formBtn');

//VALIDATIONS
let cedulaValidation = false;
let nameValidation = false;
let apellidoValidation = false;
let telfValidation = false;
let emailValidation = false;
let passwordValidation = false;
let matchValidation = false;

//GLOBAL FUNTION 
const validation = (input, regexValidation) => {
    formBtn.disabled = cedulaValidation && nameValidation && apellidoValidation && telfValidation && emailValidation && passwordValidation && matchValidation ? false:true;
    if (input.value === '') {
        input.classList.add('focus:outline-indigo-500');
        input.classList.remove('focus:outline-green-500');
        input.classList.remove('focus:outline-red-500');
    } else if (regexValidation) {
        input.classList.remove('focus:outline-indigo-500');
        input.classList.add('focus:outline-green-500',  'border-b-2');
    } else if (!regexValidation){
        input.classList.remove('focus:outline-indigo-500');
        input.classList.add('focus:outline-red-500', 'border-b-2');
    }
}


//REGEX VALIDATIONS
const REGEX_EMAIL_VALIDATION= /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/;
const REGEX_NAME_VALIDATION= /^(([A-ZÁÉÍÑÓ]{1}[a-záéíñóúü]*)|([A-ZÁÉÍÑÓ]{1}[a-záéíñóúü]*,\s(de))|(((((de)|(del)|(De)|(Del)|(la)|(las)|(los))\s)?){1,2}([A-ZÁÉÍÑÓ]{1}[a-záéíñóúü\.]*))|([A-ZÁÉÍÑÓ]{1}[a-záéíñóúü]*\s)(((((de)|(del)|(De)|(Del)|(la)|(las)|(los))\s)?){1,2}([A-ZÁÉÍÑÓ]{1}[a-záéíñóúü\.]*)))$/;
const REGEX_PASSWORD_VALIDATION= /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$/;
const REGEX_APELLIDO_VALIDATION=/^(([A-ZÁÉÍÑÓ]{1}[a-záéíñóúü]*)|([A-ZÁÉÍÑÓ]{1}[a-záéíñóúü]*,\s(de))|(((((de)|(del)|(De)|(Del)|(la)|(las)|(los))\s)?){1,2}([A-ZÁÉÍÑÓ]{1}[a-záéíñóúü\.]*))|([A-ZÁÉÍÑÓ]{1}[a-záéíñóúü]*\s)(((((de)|(del)|(De)|(Del)|(la)|(las)|(los))\s)?){1,2}([A-ZÁÉÍÑÓ]{1}[a-záéíñóúü\.]*)))$/;
const REGEX_CEDULA_VALIDATION =/^[0-9]{5,9}$/
const REGEX_TELF_VALIDATION =/^(0414|0424|0412|0416|0426)[0-9]{7}$/


//EVENTS//

//CEDULA EVENT
cedula.addEventListener('input', e  =>  {
    cedulaValidation= REGEX_CEDULA_VALIDATION.test(e.target.value);
    validation(cedula, cedulaValidation);
});

//NAME EVENT
Name.addEventListener('input', e  =>  {
    nameValidation= REGEX_NAME_VALIDATION.test(e.target.value);
    validation(Name, nameValidation);
});

// APELLIDO EMAIL
apellido.addEventListener('input', e  =>  {
    apellidoValidation= REGEX_APELLIDO_VALIDATION.test(e.target.value);
    validation(apellido, apellidoValidation);
});

//EMAIL EVENT
email.addEventListener('input', e  =>  {
    emailValidation= REGEX_EMAIL_VALIDATION.test(e.target.value);
    validation(email, emailValidation);

});

//TELEFONO EVENT
telef.addEventListener('input', e  =>  {
    telfValidation= REGEX_TELF_VALIDATION.test(e.target.value);
    validation(telef, telfValidation);

});

//PASSWORD EVENT
password.addEventListener('input', e  =>  {
    passwordValidation= REGEX_PASSWORD_VALIDATION.test(e.target.value);
    matchValidation= e.target.value === match.value;
    validation(password, passwordValidation);
    validation(match, matchValidation);
});

// MATCH PASSWORD EVENT
match.addEventListener('input', e  =>  {
    matchValidation= e.target.value === password.value;
    validation(match, matchValidation);
});

