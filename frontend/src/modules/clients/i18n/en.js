export default {
  page: {
    eyebrow: 'Clients',
    title: 'Manage your clients',
    loading: 'Loading clients...',
    empty: 'No clients yet.',
    actions: {
      create: 'Create client',
      edit: 'Edit',
      archive: 'Archive'
    },
    badges: {
      favourite: 'Favourite'
    }
  },
  modal: {
    titleCreate: 'Create client',
    titleEdit: 'Edit client',
    optional: 'Optional'
  },
  fields: {
    name: 'Name',
    address: 'Address',
    city: 'City',
    country: 'Country',
    mainContactMethod: 'Main contact method',
    mainContact: 'Main contact',
    additionalContact: 'Additional contact',
    ico: 'IČO',
    dic: 'DIČ',
    notes: 'Notes'
  },
  contactMethods: {
    email: 'Email',
    whatsapp: 'WhatsApp',
    discord: 'Discord'
  },
  validation: {
    nameRequired: 'Name is required',
    nameTooLong: 'Name must be at most {max} characters',
    addressRequired: 'Address is required',
    addressTooLong: 'Address must be at most {max} characters',
    cityRequired: 'City is required',
    cityTooLong: 'City must be at most {max} characters',
    countryRequired: 'Country is required',
    countryTooLong: 'Country must be at most {max} characters',
    contactMethodRequired: 'Contact method is required',
    mainContactRequired: 'Main contact is required',
    mainContactTooLong: 'Main contact must be at most {max} characters',
    additionalContactTooLong: 'Additional contact must be at most {max} characters',
    icoTooLong: 'IČO must be at most {max} characters',
    dicTooLong: 'DIČ must be at most {max} characters',
    notesTooLong: 'Notes must be at most {max} characters'
  },
  toasts: {
    created: 'Client created',
    updated: 'Client updated',
    archived: 'Client archived'
  },
  errors: {
    load: 'Unable to load clients.',
    save: 'Unable to save client.',
    archive: 'Unable to archive client.'
  },
  hints: {
    favourite: 'Toggle favourite client'
  }
}
