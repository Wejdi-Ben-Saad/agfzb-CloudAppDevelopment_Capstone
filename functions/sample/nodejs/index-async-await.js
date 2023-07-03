/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

params ={
  "COUCH_URL": "https://5d41420a-407f-422a-9d84-aac17084e0b5-bluemix.cloudantnosqldb.appdomain.cloud",
  "IAM_API_KEY": "fPv4gVmYNVCTv5GBXxro7aOql4HkM_urScFwbriL6Xt-"
}

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
