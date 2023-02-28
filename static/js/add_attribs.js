
                    function clicAddAttribute(){
                        // create a new div element
                        const contenedor = document.getElementById("atributoContenedor");
                       
                        const newDiv = document.createElement("div");

                        const newlabel = document.createElement("label");
                        newlabel.className = "form-label";
                        newlabel.textContent = "Atributo";

                        const newInput = document.createElement("input");
                        newInput.className = "form-control";
                        newInput.type="text";

                        const newlabelValue = document.createElement("label");
                        newlabelValue.className = "form-label";
                        newlabelValue.textContent = "Valor";

                        const valueInput = document.createElement("input");
                        valueInput.className = "form-control";
                        valueInput.type= "text";
                       
                       
                        newDiv.appendChild(newlabel);
                        newDiv.appendChild(newInput);

                        newDiv.appendChild(newlabelValue);
                        newDiv.appendChild(valueInput);

                        contenedor.appendChild(newDiv);
                    }
                    