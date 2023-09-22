const getList = async () => {
  let url = 'http://127.0.0.1:5000/madeiras';
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      data.madeiras.forEach(item => insertList(item.madeira, item.volume, item.produto, item.origem));
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

const postItem = async (inputMadeira, inputVolume, inputProduto, inputOrigem) => {
  const formData = new FormData();
  formData.append('madeira', inputMadeira);
  formData.append('volume', inputVolume);
  formData.append('produto', inputProduto);
  formData.append('origem', inputOrigem);

  let url = 'http://127.0.0.1:5000/madeira';
  fetch(url, {
    method: 'post',
    body: formData
  })
    .then((response) => response.json())
    .then((data) => {
      // Faça algo com a resposta do servidor, se necessário
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

  const insertButton = (parent) => {
    let span = document.createElement("span");
    let txt = document.createTextNode("\u00D7");
    span.className = "close";
    span.appendChild(txt);
    parent.appendChild(span);
  }

 const removeElement = () => {
    let close = document.getElementsByClassName("close");
   // var table = document.getElementById('myTable');
    let i;
    for (i = 0; i < close.length; i++) {
          close[i].onclick = function () {
        let div = this.parentElement.parentElement;
        const madeiraItem = div.getElementsByTagName('td')[0].innerHTML
        if (confirm("Você tem certeza?")) {
          div.remove()
          deleteItem(madeiraItem)
          alert("Madeira Removida!")
        }
      }
    }
  }


  const deleteItem = (item) => {
    console.log(item)
    let url = 'http://127.0.0.1:5000/paciente?nome=' + item;
    fetch(url, {
      method: 'delete'
    })
      .then((response) => response.json())
      .catch((error) => {
        console.error('Error:', error);
      });
  }

  const newItem = () => {
    let inputMadeira = document.getElementById("newMadeira").value;
    let inputVolume = document.getElementById("newVolume").value;
    let inputProduto = document.getElementById("newProduto").value;
    let inputOrigem = document.getElementById("newOrigem").value;

    if (inputMadeira === '') {
      alert("Escreva o nome de uma madeira!");
    } else if (isNaN(inputVolume)) {
      alert("Volume precisa ser em número!");
    } else {
      insertItem(inputMadeira, inputVolume, inputProduto, inputOrigem)
      postItem(inputMadeira, inputVolume, inputProduto, inputOrigem)
      alert("Madeira adicionada!")
    }
  }


const insertItem = (madeira, volume, produto, origem) => {
  var item = [madeira, volume, produto, origem];
  var table = document.getElementById('myTable');
  var row = table.insertRow();

  for (var i = 0; i < item.length; i++) {
    var cel = row.insertCell(i);
    cel.textContent = item[i];
  }
  insertButton(row.insertCell(-1));
  document.getElementById("newMadeira").value = "";
  document.getElementById("newVolume").value = "";
  document.getElementById("newProduto").value = "";
  document.getElementById("newOrigem").value = "";

  removeElement();
}

