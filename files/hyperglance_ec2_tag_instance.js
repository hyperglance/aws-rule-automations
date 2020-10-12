const AWS = require('aws-sdk');

exports.handler = async (event) => {
    const hgAlert = JSON.parse(event.Records[0].Sns.Message);
    
    console.log(
        'Received Hyperglance alert from saved-search.\n',
        '( ',
        'Name: ', hgAlert.name, '\n',
        'Pack: ', hgAlert.pack, '\n',
        'Description: ', hgAlert.description, '\n',
        'Status: ', hgAlert.status, '\n',
        'Threshold: ', hgAlert.threshold, '\n',
        'Evaluation Time: ', hgAlert.evaluatedAt, '\n',
        'Num Results: ', hgAlert.results.length,
        ' )'
    );
    
    // we only care about threshold breaches
    if (hgAlert.status !== 'ABOVE_THRESHOLD' &&
        hgAlert.status !== 'BELOW_THRESHOLD') {
            console.log('Status was ', hgAlert.status, ', so exiting with nothing to do');
            return;
    }
    
    await processEachRegion(hgAlert, async (region, resourceIDs) => {
        const EC2 = new AWS.EC2({apiVersion: '2016-11-15', region});
        // TAGGING
        const tagParams = {
            Resources: resourceIDs,
            /* Tags are defined as key / value pairs. Each pair is contained in a set of braces {}
            Update the below tag definitions to your own standards, each pair of braces is separated by a comma (,) */
            Tags: [
              {
                Key: 'HyperglanceTest', 
                Value: 'HyperglanceTest'
              },
              {
                Key: 'Description',
                Value: 'Tag Added By Hyperglance'
              },
              {
                Key: 'Your Tag',
                Value: 'Your Value'
              }
            ]
        };

        await EC2.createTags(tagParams).promise();
        
    });
};

async function processEachRegion(hgAlert, callback) {
    // group resource IDs up according to their region
    const resourcesByRegion = hgAlert.results.reduce(
        (map, res) => {
            const ids = map.get(res.region) || [];
            ids.push(res.id);
            return map.set(res.region, ids);
        }, new Map());
    
    // connect to each region and issue the request
    for (const [region, resourceIDs] of resourcesByRegion.entries()) {
        await callback(region, resourceIDs);
    }
}