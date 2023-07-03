/**
 * Get all databases
 */

 const { CloudantV1 } = require("@ibm-cloud/cloudant");
 const { IamAuthenticator } = require("ibm-cloud-sdk-core");
 
 params ={
  "COUCH_URL": "https://5d41420a-407f-422a-9d84-aac17084e0b5-bluemix.cloudantnosqldb.appdomain.cloud",
  "IAM_API_KEY": "fPv4gVmYNVCTv5GBXxro7aOql4HkM_urScFwbriL6Xt-"
}
 
 function main(params_dict) {
   const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
   const cloudant = CloudantV1.newInstance({
     authenticator: authenticator,
   });
   cloudant.setServiceUrl(params.COUCH_URL);
 
   let dbList = getDbs(cloudant);
   return { dbs: dbList };
 }
 
 function getDbs(cloudant) {
   cloudant
     .getAllDbs()
     .then((body) => {
       body.forEach((db) => {
         dbList.push(db);
       });
     })
     .catch((err) => {
       console.log(err);
     });
 }