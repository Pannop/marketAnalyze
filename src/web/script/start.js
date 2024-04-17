var marketListChecks = document.getElementById("marketListChecks");
var marketListCheck_from = document.getElementById("marketListCheck_from");
var marketListCheck_to = document.getElementById("marketListCheck_to");
var baseData = null;

eel.expose(setSize);
function setSize(width, height) {

    let html = document.getElementById("html");
    html.style.width = `${width}px`;
    html.style.height = `${height}px`;
    window.resizeTo(width, height);
}


function setMarketList(index, marketList) {
    addMarketCheckBox = (name) => {
        return `
        <div class="form-check">
            <input class="form-check-input" type="checkbox" id="marketListCheck_${name}" value="${name}" onchange="drawMarketChart();">
            <label class="form-check-label" for="flexCheckDefault">
                ${name}
            </label>
        </div>
        `
    }
    str = addMarketCheckBox(index);
    for (let i = 0; i < marketList.length; i++) {
        str += addMarketCheckBox(marketList[i]);
    }
    marketListChecks.innerHTML = str;
}

eel.expose(setData);
function setData(data) {
    baseData = data;
    setMarketList(baseData["indexName"], baseData["marketList"]);
}


eel.setDefaultSize();
eel.loadData();


function getSelectedMarkets() {
    selected = [];
    checks = marketListChecks.children;
    for (let i = 0; i < checks.length; i++) {
        if (checks[i].children[0].checked)
            selected.push(checks[i].children[0].value);
    }
    return selected;
}

function marketListSetAll(checked) {
    checks = marketListChecks.children;
    for (let i = 0; i < checks.length; i++) {
        checks[i].children[0].checked = checked;
    }
    drawMarketChart();
}

google.charts.load('current', { packages: ['corechart', 'line'] });
google.charts.setOnLoadCallback(drawMarketChart);

var drawing = false;
var data;
function drawMarketChart() {
    selected = getSelectedMarkets();
    if(!drawing && selected.length>0){
        drawing = true;
        data = new google.visualization.DataTable();

        data.addColumn('number', 'x');
        selected.forEach(element => {
            data.addColumn('number', element);
        }); 

        interval = document.querySelector('input[name="marketListCheck_radioInterval"]:checked').value;

        

        eel.formatData(selected, marketListCheck_from.value, marketListCheck_to.value, interval);
    
        
    }

}


eel.expose(applyMarketChart);
function applyMarketChart(formattedData){
    console.log("drawing")
    console.log(formattedData)
    data.addRows(formattedData);

    var options = {
        hAxis: {
            title: 'Time'
        },
        vAxis: {
            title: 'Close'
        }
    };

    var chart = new google.visualization.LineChart(document.getElementById('marketChart'));
    chart.draw(data, options);
    drawing = false;
}






