


const dict_leg_to_en = {
  'ab initio': 'from the beginning',
  'dispute resolution': 'methods to resolve a dispute without going to court',
  'adr': 'methods to resolve a dispute without going to court',
  'arbitration': 'private dispute resolution with arbiter ',
  'assignment': 'parties may transfer away liabilities or rights',
  'novation': 'parties may transfer away liabilities or rights',
  'bankruptcy': 'the inability to repay debt',
  'bankrupt': 'the inability to repay debt',
  'bona fide': 'in good faith',
  'breach': 'when a party fails to comply width the contract',
  'caveat emptor': 'buyer beware',
  'confidential': 'secret',
  'counterpart': 'copy',
  'counterparts': 'copy',
  'cure period': 'time given to correct a violation of a contract',
  'damages': 'money owed when a contract is breached',
  'damage': 'money owed when a contract is breached',
  'deed': 'legally binding contract',
  'deeds': 'legally binding contracts',
  'default': 'the situation when one party is in breach of the contract',
  'defaults': 'the situation when one party is in breach of the contract',
  'deliverables': 'things a party needs to supply',
  'deliverable': 'things a party needs to supply',
  'entire agreement': 'the contract is understood by all parties',
  'express terms': 'the terms agreed to in the contract',
  'express term': 'the terms agreed to in the contract',
  'force majeure': 'the conditions where the a party is unable to abide by the contract',
  'governing law': 'the geographic law of that governs a contract',
  'governing laws': 'the geographic law of that governs a contract',
  'implied terms': 'terms that are not written down',
  'implied term': 'terms that are not written down',
  'indemnity': 'liability payment',
  'compliance': 'determines if the goods or services produced meet the terms',
  'commitment': 'the result of entering an agreement',
  'frustration': 'end the contract if the requirements become illegal',
  'injunction': 'a court order to make or stop a party from doing something',
  'intellectual property': 'the ownership of non-physical work, such as art or patents',
  'joint liability': 'the parties are partners, and may share responsibilities',
  'several liability': 'the parties are partners, and may share responsibilities',
  'jurisdiction': 'the place where disputes can be submitted',
  'key performance': 'a method to determine how well the agreements made are progressing',
  'limited liability': 'liability may have a maximum amount that can be paid',
  'liquidation': 'selling assets or property',
  'litigation': 'the use of court to solve disputes',
  'mala fide': 'in bad faith',
  'material breach': 'a serious violation of contract',
  'mediation': 'dispute resolution that uses a neutral third party',
  'obligation': 'things that have to be done',
  'obligations': 'things that have to be done',
  'party': 'the people or groups that sign a contract',
  'parties': 'the peoples or groups that sign a contract',
  'period': 'length of time',
  'bid': 'offer to supply goods or services',
  'bids': 'offers to supply goods or services', 
  'appraisal': 'assesses the value of an offer to supply goods or services',
  'appraisals': 'assesses the value of an offer to supply goods or services',
  'conditioning': 'determines if the offer to supply goods or services meets the agreement',
  'pro rata': 'the rate',
  'pro tempore': 'for the time being',
  'pro tem': 'for the time being',
  'quid pro quo': 'something for something',
  'recitals': 'reasons for entering the agreement',
  'recital': 'reasons for entering the agreement',
  'background': 'reasons for entering the agreement',
  'preamble': 'reasons for entering the agreement',
  'remedies': 'things that can be done to address a breach of contract',
  'remedy': 'things that can be done to address a breach of contract',
  'representations': 'factual statements or promises made by one party to another',
  'representation': 'factual statement or promise made by one party to another',
  'risk of loss': 'the risks and responsibilities if certain things are damaged',
  'severability': 'the ability to remove disqualifying sections of a contract',
  'termination': 'rules for when the contract can be ended',
  'third party': 'a person or group that is neutral',
  'third parties': 'groups that are neutral',
  'variation': 'ways to edit the contract after it has been signed',
  'variations': 'ways to edit the contract after it has been signed',
  'void': 'not legally binding',
  'waiver': 'an agreement that removes certain rights',
  'warranties': 'promises',
  'warranty': 'promise',
  'guaranty': 'makes a person or group outside the contract responsible',
  'license': 'rules for how to use property',
  'licenses': 'rules for how to use property',
  'amidst': 'amid',
  'amongst': 'among',
  'aforementioned': 'that/these',
  'as to': 'about',
  'hereby': '',
  'herein': 'within this',
  'hereinabove': 'above',
  'hereinbefore': 'above',
  'hereinafter': 'below',
  'hereto': '',
  'hereunder': 'under this',
  'in lieu of': 'instead of',
  'instant case': 'here',
  'inter alia': 'among other things',
  'mutatis mutandis': 'with the necessary changes',
  'disclaimer': 'a statement that denies responsibility',
  'pari passu': 'equally',
  'per annum': 'each year',
  'prima facie': 'it appears',
  'said': 'the',
  'same': 'it',
  'set forth': 'set out',
  'such': 'that',
  'thereafter': 'later',
  'therein': 'inside',
  'thereof': 'because of that',
  'thereto': 'about',
  'whilst': 'while',
};


const legal_to_eng = (sentenceList) => {

  lst = document.getElementById('summ');
  

  for(sentence of sentenceList){
    let words = sentence.split(" ");
    words = words.map((i) => i.replace(/\W/g, ''));
    for(let i = 0; i < words.length; i++){
      if(((i + 1) < words.length) && (dict_leg_to_en[(String(words[i]).toLowerCase() + ' ' + String(words[i+1]).toLowerCase())])){
        words[i] = `<div class="tooltip">${words[i] + " " + words[i + 1]}<span class="tooltiptext">${String(dict_leg_to_en[(String(words[i]).toLowerCase() + ' ' + String(words[i+1]).toLowerCase())])}</span></div>`
        words[i+1] = '';
        i ++;
      } 
      else if (dict_leg_to_en[String(words[i]).toLowerCase()]){
        words[i] = `<div class="tooltip">${words[i]}<span class="tooltiptext">${String(dict_leg_to_en[(String(words[i]).toLowerCase())])}</span></div>`
      }
    }
    sen = words.join(' ');
    tst = lst.appendChild( document.createElement('li'));
    tst.className += 'itm';
    tst.innerHTML = sen;
  }
}

