
//let dropdown = getElementById("date_options");
//let mac_input = getElementById('mac_input').value
//dropdown.innerHTML = '';
//let response = await fetch('http://127.0.0.1:5000/get_by_mac?mac='+mac_input);
////        wait for the response to come and put the text of response in data
//let data = await response.json();
//data.forEach(function (date) {
//let option = document.createElement('option');
//option.text=date ;
//dropdown.add(option);});


async function get_mac(){
    try {
        let macs_res = await fetch('http://127.0.0.1:5000/get_macs');
        let macs = await macs_res.json();
        document.getElementById('macs_list').textContent=macs;
    }
    catch (error) {
        console.error(error);
    }
}

let current_mac = ''
async function get_by_mac(){
    try {
        let mac_input = document.getElementById('mac_input').value;
        current_mac = mac_input
//        wait for the response and put it in response
        let response = await fetch('http://127.0.0.1:5000/get_by_mac?mac='+mac_input);
//        wait for the response to come and put the text of response in data
        let data = await response.json();
//        print to console
        console.log(data);

        let dropdown = document.getElementById("date_options");

        dropdown.innerHTML = '';

        data.forEach(function (date) {
        let option = document.createElement('option');
        option.text=date ;
        dropdown.add(option);
        });

    } catch (error) {
        console.error(error);
    }
}



async function get_by_date(){
    try {
        let date_input = document.getElementById('date_options');
        let select_date = date_input.options[date_input.selectedIndex].value;

        console.log(select_date);
        let response = await fetch('http://127.0.0.1:5000/get_by_date?date='+select_date+'&mac='+current_mac);
        let data = await response.text();
        console.log(data);
        document.getElementById('data').textContent=data;
        console.log(response.ok);

    } catch (error) {
        console.error(error);
    }
}


async function stop(){
    try{
        let mac = document.getElementById('mac_input').value;
        let response = await fetch('http://127.0.0.1:5000/stop?mac='+current_mac)
//    method: 'POST',
//    headers: {
//                'Content-Type': 'application/json'
//            },
//    body: JSON.stringify({
//        mac: mac
//    })
//})
        const text = await response.text();
        document.getElementById('stop_message').textContent = text;
}
        catch (error) {
        console.error(error);}
}


document.addEventListener('DOMContentLoaded', () => {
    get_mac();
});