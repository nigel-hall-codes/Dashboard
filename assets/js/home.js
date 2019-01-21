var BotApp = angular.module('BotApp', []);

BotApp.controller('BotAppCtrl', ['$scope', function($scope) {

     $( document ).ready(function() {
            console.log("Hello")
            retrieveBotStats()
            console.log($scope.bot_stats)
     });

     $scope.test = function($event) {
        console.log($event.target.textContent)
        $scope.timeperiod = $event.target.textContent
        retrieveBotStats()

     }

    $scope.data = "data";
    $scope.bots = [{"name": "bot1", "return": ".35%"}, {"name": "bot2", "return": ".45%"}]
    $scope.timeperiod = 'Day'



    function retrieveBotStats() {
         var xhr = new XMLHttpRequest();
                xhr.onreadystatechange = function () {
                    if (xhr.readyState == XMLHttpRequest.DONE) {

                        response = JSON.parse(xhr.responseText);
                        console.log(response);
                        $scope.bot_stats = response

                        // console.log($scope.bot_stats[0])
                        $scope.loaderHide = true;
                        $scope.$apply()
                    }
                };
                xhr.open('POST', "http://127.0.0.1:8000" + '/api/botstats/', true);
                xhr.setRequestHeader("Content-Type", "application/json");
                xhr.send(JSON.stringify({'timeperiod': $scope.timeperiod}))
            }


}])


