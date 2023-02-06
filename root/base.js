function clearInput(listOfIds) {
    listOfIds.forEach (id => {
        var getValue = document.getElementById(id);
        if (getValue.value !="") {
            getValue.value = "";
        }
    })
}

function createOutput(response, weatherElement) {
    var element = document.getElementById(weatherElement)
    element.textContent = response
}

$(document).ready(function() {
        
    document.querySelector('#get-weather').addEventListener('click', async () => {
        $("#error").css("display", "none");

        let input = document.getElementById("user-input");

        const response = await fetch(`/api/get-weather/${input.value}`, 
            {
                headers: {
                    "Content-Type": "application/json",
                },
            })
        
        const res = await response.json()
        console.log(res)
        
        let locationIcon = document.querySelector('.weather-icon');

        if (res.error) {
            clearInput(['closest-matching-address', 'description', 'temperature', 'feels_like'])
            createOutput(`Could not find coordinates for ${input.value}`, "error")
            $("#error").css("display", "block");
            locationIcon.innerHTML = `<img src="/static/icons/unknown.png">`;
        
        }
        else {
            createOutput(res.address, "closest-matching-address")
            createOutput(res.description, "description")
            createOutput(res.temperature, "temperature")
            createOutput(res.feels_like, "feels_like")
            createOutput(res.symbol, "temp-symbol")
            createOutput(res.symbol, "feels-symbol")
            const icon = res.icon;
            locationIcon.innerHTML = `<img src="/static/icons/${icon}.png">`;
        }
        
        input.value= "";
        
    })

    document.querySelector('#save-weather').addEventListener('click', async () => {

        let address = document.getElementById("closest-matching-address").innerHTML
        let description = document.getElementById("description").innerHTML
        let temperature = document.getElementById("temperature").innerHTML
        let feels_like = document.getElementById("feels_like").innerHTML
        let symbol = document.getElementById("temp-symbol").innerHTML
    
        $.ajax({
            type: "GET",
            url: `/home`,
            data: {
                "address": address,
                "description": description,
                "temperature": temperature,
                "feels_like": feels_like,
                "symbol": symbol
            },
            dataType: "json",
        });
    })

    document.querySelector('#historical-data').addEventListener('click', async () => {

        table_body = document.getElementById("dynamic-info")
        table_body.innerHTML = ""

        const response = await fetch(`/api/get-historical-data`, 
        {
            headers: {
                "Content-Type": "application/json",
            },
        })
        const res = await response.json()

        console.log(res)

        $("#historical-data-table").css("display", "block");
    
        $.each(res, function(i, item) {
            var $tr = $("<tr>").append(
                $('<td id="address">').text(item.address),
                $('<td id="temp-description">').text(item.description),
                $('<td id="temp">').text(item.temperature),
                $('<td id="feels-like">').text(item.feels_like),
                $('<td id="symbol">').text(item.symbol)
            ).appendTo(table_body);
        });

       
    })
})