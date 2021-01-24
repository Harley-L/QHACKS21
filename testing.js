require('dcp-client').initSync();

const compute = require('dcp/compute');

var bigDecimal = require('js-big-decimal');


async function start(){



    let job = compute.for(1,3, function(n){
        progress();



        try{
            function factorial(num) {
                var big = new bigDecimal(num);
                if (bigDecimal.compareTo(big.getValue(), 0) == -1) return 1;
                else if (bigDecimal.compareTo(big.getValue(), 0) == 0) return 1;
                else {
                    progress();
                    return (bigDecimal.multiply(big.getValue(), factorial(bigDecimal.subtract(big.getValue(), "1"))));
                }
            }
        } catch(err){
            console.log("Error", err.stack);
            console.log("Error", err.name);
            console.log("Error", err.message);
        }


        try{
            progress();
            var value = factorial(n);
            return value;
        }catch(err){
            console.log("Error", err.stack);
            console.log("Error", err.name);
            console.log("Error", err.message);
        }

    }, [bigDecimal]());


    job.public.name = ("Factorial Calculations");
    job.on('accepted', () => {
        console.log('Job accepted: ' + job.id);
    });

    job.on('console', (event) => console.log(event));

    job.on('status', (status) => {
        console.log('STATUS:');
        console.log(
            status.total + ' slices posted, ' +
            status.distributed + ' slices distributed, ' +
            status.computed + ' slices computed.'
        );
    });


    var sum = 0;
    job.on('result', (thisOutput) => {
        console.log('RESULT:');
        console.log(thisOutput.result);
        sum = sum+thisOutput.result;
    });

    job.on('error', (event) => {
        console.error('An exception was thrown by the work function:', event.message);
    });

    job.on('complete', () => {
        console.log('Done');
        console.log(sum);
    });

    try{
        console.log("doing the thing");
        await job.exec();
    } catch(myError){
        console.log("Failed.")
    }

}//end of start();

start();