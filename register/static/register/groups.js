document.addEventListener("DOMContentLoaded", function() {

    const button = document.querySelectorAll('.btn-check');
    const locationView = document.querySelector('#locations');
    const detailedView = document.querySelector('#detailed');
    const selectLocationView = document.querySelector('#selectLocation');
    const groupsView = document.querySelector('#groups');
    const saveButton = document.querySelector('#button-addon2');
    const locationOption = document.querySelector('#locationOption');

    var subject = "main";

    // Create a list of areas on location change
    locationOption.onchange = function()
    {
        // Query database for areas in selected location
        const locationName = locationOption.value;
        fetch(`/data?q=${locationName}`)
        .then(response => response.json())
        .then(data => {

            // Erase list and populate with areas from selected location 
            let list = "";
            for (let area in data.areas) {
                console.log(data.areas[area]);
                list += "<li>" + data.areas[area] + "</li>";
                
            }
            
            // Show list in HTML document
            document.querySelector('#areas').innerHTML = list; 
            
        })
    }
   

    saveButton.addEventListener("click", function() {
        const newItem = document.querySelector('#addNew').value;
        const token = document.querySelector("input[name='csrfmiddlewaretoken']").value;
        console.log(newItem);
        console.log(token);
        console.log(subject);

        // Save new location into database
        if (subject == "main") {
            fetch('/machines/locations', {
                method: 'POST',
                headers: { "X-CSRFToken": token },
                body: JSON.stringify({
                    subject: subject,
                    item: newItem
                })
            })
            .then( () => {
                const li = document.createElement('li');
                li.className = "newElement";
                li.innerHTML = newItem;
                document.querySelector('#names').append(li);
            })

        }

        // Save new area into database  
        if (subject == "areas") {
            fetch('/machines/locations', {
                method: 'POST',
                headers: { "X-CSRFToken": token },
                body: JSON.stringify({
                    subject: subject,
                    location: locationOption.value,
                    item: newItem
                })
            })
            .then( () => {
                const li = document.createElement('li');
                li.className = "newElement";
                li.innerHTML = newItem;
                document.querySelector('#areas').append(li);
            })

        }

        // Save new group into database
        if (subject == "groups") {
            fetch('/machines/locations', {
                method: 'POST',
                headers: { "X-CSRFToken": token },
                body: JSON.stringify({
                    subject: subject,
                    item: newItem
                })
            })
            .then( () => {
                const li = document.createElement('li');
                li.className = "newElement";
                li.innerHTML = newItem;
                document.querySelector('#groupList').append(li);
            })
        }
       
    })
  
    button.forEach(function(button) {
        button.onclick = function() {
            console.log(button.id);
            if (button.id == "btnradio1") {
                locationView.style.display="block"
                detailedView.style.display="none";
                groupsView.style.display="none";
                selectLocationView.style.display="none";

                subject = "main";
            }

            if (button.id == "btnradio2") {
                locationView.style.display="none"
                detailedView.style.display="block";
                groupsView.style.display="none";
                selectLocationView.style.display="block";

                subject = "areas";
            }

            if (button.id == "btnradio3") {
                locationView.style.display="none"
                detailedView.style.display="none";
                groupsView.style.display="block";
                selectLocationView.style.display="none";

                subject = "groups";
            }
        }
    })
})