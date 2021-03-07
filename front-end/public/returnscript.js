


const dict_leg_to_en = {
  'ab initio': 'from the beginning',
  'alternative dispute resolution': 'methods to resolve a dispute without going to court',
  'ADR': 'methods to resolve a dispute without going to court',
  'arbitration': 'private dispute resolution without going to court',
  'assignment': 'parties may transfer away liabilities or rights',
  'novation': 'parties may transfer away liabilities or rights',
  'bankruptcy': 'the inability to repay debt',
  'bona fide': 'in good faith',
  'breach of contract': 'when a party fails to comply to the contract',
  'caveat emptor': 'buyer beware',
  'confidential': 'secret',
  'counterpart': 'copy',
  'cure period': 'time given to correct a violation of a contract',
  'damages': 'money given when a contract is broken',
  'deed': 'legally binding contract',
  'default': 'the situation when one party breaks the contract',
  'deliverables': 'things a party needs to supply',
  'entire agreement': 'the contract is understood by all parties',
  'express terms': 'the terms agreed to in the contract',
  'force majeure': 'the conditions where the a party is unable to abide by the contract',
  'governing law': 'the laws of your city, county, or state',
  'implied terms': 'terms that are not written down',
  'indemnity': 'liability payment',
  'injunction': 'a court order to make or stop one group from doing something',
  'intellectual property': 'the ownership of non-physical work, such as art or patents',
  'joint liability': 'the parties are partners, and may share responsibilities',
  'several liability': 'the parties are partners, and may share responsibilities',
  'jurisdiction': 'the place where disputes can be submitted',
  'key performance': 'a method to determine if how well the agreements made are progressing',
  'limited liability': 'liability may have a maximum amount that can be paid',
  'liquidation': 'selling assets or property',
  'litigation': 'the use of court to solve disputes',
  'mala fide': 'in bad faith',
  'material breach': 'a serious violation of contract',
  'mediation': 'dispute resolution that uses a neutral person or group',
  'obligation': 'things that have to be done',
  'party': 'the people or groups that sign this contract',
  'period': 'length of time',
  'pro rata': 'the rate',
  'pro tempore': 'for the time being',
  'pro tem': 'for the time being',
  'quid pro quo': 'something for something',
  'recitals': 'reasons for entering the agreement',
  'background': 'reasons for entering the agreement',
  'preamble': 'reasons for entering the agreement',
  'remedies': 'things that can be done to reverse a breach of contract',
  'representations': 'factual statements or promises made by one party to another',
  'risk of loss': 'the risks and responsibilities if certain things are damaged',
  'severability': 'the ability to edit the contract if an agreement is illegal',
  'termination': 'rules for when the contract can be ended',
  'third party': 'a person or group that is neutral',
  'variation': 'ways to edit the contract after it has been signed',
  'void': 'not legally binding',
  'waiver': 'an agreement that removes certain rights',
  'warranties': 'promises',
  'guaranty': 'makes a person or group outside the contract responsible',
  'license': 'rules for how to use property',
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

