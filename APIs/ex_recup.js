$(document).ready(function(){
    $("#get").click(function(){
        var city = $("#city").val(); 
        var url ="http"+city+"suite";

        $.get(url,function(data) {
            //peut mtn sélectionner les valeurs voulus 
            //selon le retour, dépend de l'api, ex:
            var description = data.weather[0].description;
            var temp = data.main.temp;
        $("#rep").append(description + "<br />" + temp)
        })
    }); 
})