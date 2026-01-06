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
    addressRequired: 'Address is required',
    cityRequired: 'City is required',
    countryRequired: 'Country is required',
    contactMethodRequired: 'Contact method is required',
    mainContactRequired: 'Main contact is required'
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
