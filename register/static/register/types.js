document.addEventListener("DOMContentLoaded", function() {

    const manufacturerSelect = document.querySelector('#manufacturer-select')
    const selectTypeView = document.querySelector('#typeSelect');
    const TypeOption = document.querySelector('#machineType');

    manufacturerSelect.onchange = function () {
        const manufacturer = manufacturerSelect.value;
        console.log(manufacturer);
        fetch(`/data?mfr=${manufacturer}`)
        .then(response => response.json())
        .then(data => {
            console.log(data.types);
            let list = "";
            for (let type in data.types) {
                list += "<option>" + data.types[type] + "</option>";
                
            }
            console.log(list);
            document.querySelector('#machineType').innerHTML = list;

        })
    }
})