function clicAddAttribute(e){
    // create a new div element
    const contenedor = document.getElementById("nuevosAtributos");
  
    const newDiv = document.createElement("div");
    newDiv.id = "atributoContenedor";

    const newlabel = document.createElement("label");
    newlabel.className = "form-label fw-bold";
    newlabel.textContent = "Atributo";        

    const newInput = document.createElement("input");
    newInput.className = "form-control";
    newInput.type="text";
    newInput.name="atributoNew";

    const labeltipoDato = document.createElement("label");
    labeltipoDato.className = "form-label fw-bold";
    labeltipoDato.textContent = "Tipo de dato";        
    
    const inputTipoDato = document.createElement("input");
    inputTipoDato.className = "form-control";
    inputTipoDato.type="text";
    inputTipoDato.name="tipoDatoNew";

    const atributosDisponibles = document.getElementById("id_tipodato");       
    const selectTipoDato = atributosDisponibles.cloneNode(true);
    selectTipoDato.removeAttribute("hidden");
    selectTipoDato.name = "tipoDatoNew";
    selectTipoDato.onchange = ('onchange', () => onChangeTypeData(event))


    const newlabelValue = document.createElement("label");
    newlabelValue.className = "form-label fw-bold";
    newlabelValue.textContent = "Valor";        

    const valueInput = document.createElement("input");
    valueInput.className = "form-control";
    valueInput.type= "text";
    valueInput.name= "valorNew";

    const divBarraNuevoAttribute = document.createElement("div");
   
    divBarraNuevoAttribute.id = "divBarraAtributo";

    const inputDeleteAttribute = document.createElement("input");
    inputDeleteAttribute.type = "button";
    inputDeleteAttribute.id = "deleteAttribute";
    inputDeleteAttribute.value = " -";
    inputDeleteAttribute.className = "btn btn-outline-info justify-content-between";
    inputDeleteAttribute.style = "float: right";

    inputDeleteAttribute.onclick = ('onClick',() => deleteAttribute(event))

    const minimizeAttribute  = document.createElement("input");
    minimizeAttribute.type = "button";
    minimizeAttribute.id = "minimizeAttribute";
    minimizeAttribute.className = "btn btn-outline-info justify-content-between";
    minimizeAttribute.style = "float: right";
    minimizeAttribute.value = "^";
    minimizeAttribute.onclick = ('onClick',() => showAndHide(event));

    //contenedor.appendChild(newlabel);
    divBarraNuevoAttribute.style.display = "block";

    divBarraNuevoAttribute.appendChild(newlabel);
    divBarraNuevoAttribute.appendChild(inputDeleteAttribute);
    divBarraNuevoAttribute.appendChild(minimizeAttribute);
    divBarraNuevoAttribute.appendChild(document.createElement("br"));
    divBarraNuevoAttribute.appendChild(newInput);
    

    const divContentAttribute = document.createElement("div");        
    divContentAttribute.id = "divBarraAtributo";

    divContentAttribute.appendChild(labeltipoDato);
    //divContentAttribute.appendChild(inputTipoDato);
    divContentAttribute.appendChild(selectTipoDato);
    divContentAttribute.appendChild(newlabelValue);
    divContentAttribute.appendChild(valueInput);

    divContentAttribute.style.visibility = "visible";

    newDiv.appendChild(divBarraNuevoAttribute);
    newDiv.appendChild(divContentAttribute);
    newDiv.style.visibility = "visible";
    /*newDiv.appendChild(newInput);

    newDiv.appendChild(labeltipoDato);
    newDiv.appendChild(inputTipoDato);

    newDiv.appendChild(newlabelValue);
    newDiv.appendChild(valueInput);*/

    contenedor.appendChild(newDiv);
}

function deleteAttribute(e){
   var buttonClicked = e.target;
   buttonClicked.parentElement.parentElement.remove();
}

function showAndHide(e){        
   var buttonClicked = e.target;
   var divElement = buttonClicked.parentElement;
   
   //minimizeAttribute
   var valorelem1 = document.getElementById('minimizeAttribute');
   if(divElement.parentElement.children[1].style.visibility == "visible"){
       divElement.parentElement.children[1].style.visibility = "hidden";
       divElement.parentElement.children[1].style.display = "none";
       buttonClicked.value= '˅';
   }
   else
   { 
       divElement.parentElement.children[1].style.visibility = "visible";
       divElement.parentElement.children[1].style.display = "block";
       buttonClicked.value= '˄';
   }
  
}   
function onChangeTypeData(e){
    var changeData = e.target

    e.target.parentElement.children[3].type = changeData.value
}
