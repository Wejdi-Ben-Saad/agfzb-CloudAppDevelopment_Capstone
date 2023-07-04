/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

params ={
  
}

params = require('./.creds.json');

async function main(params_dict) {
      const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
      const cloudant = CloudantV1.newInstance({
          authenticator: authenticator
      });
      cloudant.setServiceUrl(params.COUCH_URL);
      try {
        let dealershipsList = await getAllRecords(cloudant,"dealerships");
        console.log(dealershipsList);
      } catch (error) {
          return { error: error.description };
      }
}

function getAllRecords(cloudant,dbname) {
  return new Promise((resolve, reject) => {
      cloudant.postAllDocs({ db: dbname, includeDocs: true, limit: 10 })            
          .then((result)=>{
            resolve({result:result.result.rows.map(element => element.doc)
             
            });
          })
          .catch(err => {
             console.log(err);
             reject({ err: err });
          });
      })
}


main(params)
