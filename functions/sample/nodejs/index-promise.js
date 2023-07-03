/**
 * Get all dealerships;Get all dealerships by state
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

params ={
    "COUCH_URL": "https://5d41420a-407f-422a-9d84-aac17084e0b5-bluemix.cloudantnosqldb.appdomain.cloud",
    "IAM_API_KEY": "fPv4gVmYNVCTv5GBXxro7aOql4HkM_urScFwbriL6Xt-"
  }

function main(params) {

    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);

    let selector ={
    }

    if (params.hasOwnProperty("state")){
      selector["state"]=params.state
    }
    if (params.hasOwnProperty("id")){
      selector["id"]=parseInt(params.id)
    }
    
    let getDealershipsPromise = getMatchingRecords(cloudant,"dealerships",selector);
    
    return getDealershipsPromise;
}

function getDbs(cloudant) {
     return new Promise((resolve, reject) => {
         cloudant.getAllDbs()
             .then(body => {
                 resolve({ dbs: body.result });
             })
             .catch(err => {
                  console.log(err);
                 reject({ err: err });
             });
     });
 }
 
 
 /*
 Sample implementation to get the records in a db based on a selector. If selector is empty, it returns all records. 
 eg: selector = {state:"Texas"} - Will return all records which has value 'Texas' in the column 'State'
 */
 function getMatchingRecords(cloudant,dbname, selector) {
     return new Promise((resolve, reject) => {
         cloudant.postFind({db:dbname,selector:selector})
                 .then((result)=>{
                   resolve({body:result.result.docs.map(element => {delete element._id;delete element._rev;return element})});
                 })
                 .catch(err => {
                    console.log(err);
                     reject({ err: err });
                 });
          })
 }
 
                        
 /*
 Sample implementation to get all the records in a db.
 */
 function getAllRecords(cloudant,dbname) {
  return new Promise((resolve, reject) => {
      cloudant.postAllDocs({ db: dbname, includeDocs: true, limit: 10 })            
          .then((result)=>{
            resolve({body:result.result.rows.map(element => {dealership=element.doc; delete dealership._id;delete dealership._rev;return dealership})
             
            });
          })
          .catch(err => {
             console.log(err);
             reject({ err: err });
          });
      })
}

params ={
  "COUCH_URL": "https://5d41420a-407f-422a-9d84-aac17084e0b5-bluemix.cloudantnosqldb.appdomain.cloud",
  "IAM_API_KEY": "fPv4gVmYNVCTv5GBXxro7aOql4HkM_urScFwbriL6Xt-",
  "state":"Texas",
  "id": 10
}
promise1=main(params)
promise1.
  then((value) => 
    console.log(value)
  )
  .catch( err => console.log(err) );