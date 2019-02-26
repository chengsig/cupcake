const BASE_URL = "http://localhost:5000"

$(document).ready(function(){
    let $cupcakeList = $("#cupcake-list");

    async function generate_cupcake(){
        let response = await $.get(`${BASE_URL}/cupcakes`);
        let cupcakes = response.response;

        for (let cupcake of cupcakes){
            $cupcakeList.append(`<li><img src=${cupcake.image}>${cupcake.flavor} ${cupcake.size} ${cupcake.rating}</li>`)
        }
    }
    generate_cupcake();
})