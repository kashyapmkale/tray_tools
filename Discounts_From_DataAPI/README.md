This Script automates the following step:
1. Invoke v1/discounts for the venue with selectedDate -> {discountedItems}.
2. Invoke v1/revenueCenters, to get list of  training mode services (“isTrainingMode”:true)  -> trainingServicesList.
3. Invoke v1/items -> itemsList and ignore items with  revenueCenterId in trainingServicesList from Step 2-{nonTrainingItems}.
4. Filter out discounts from Step1 which do not have items from Step3 nonTrainingItems.
5. Aggregate amount field for all discountedItems from Step4.
6. Store this value.
7. From itemsList (step 3) add grossPrice for all items with “isComp”:true while excluding voided items (“voided”: true or “itemVoided”: true).
8. Add the values from step 6 and step 7 together.
