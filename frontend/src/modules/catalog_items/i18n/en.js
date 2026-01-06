export default {
  page: {
    eyebrow: 'Catalog',
    title: 'Catalog items',
    loading: 'Loading catalog items...',
    empty: 'No catalog items yet.',
    actions: {
      create: 'Create item',
      edit: 'Edit',
      archive: 'Archive'
    },
    priceLine: '{price} / {unit}',
    taxLine: 'Tax {rate}%'
  },
  modal: {
    titleCreate: 'Create catalog item',
    titleEdit: 'Edit catalog item',
    optional: 'Optional'
  },
  fields: {
    name: 'Name',
    description: 'Description',
    unit: 'Unit',
    unitPrice: 'Price per unit',
    taxRate: 'Tax rate'
  },
  validation: {
    nameRequired: 'Name is required',
    descriptionRequired: 'Description is required',
    unitRequired: 'Unit is required',
    unitPriceRequired: 'Price is required',
    unitPriceInvalid: 'Enter a valid price with up to 2 decimals',
    taxRateInvalid: 'Tax rate must be a whole number'
  },
  toasts: {
    created: 'Catalog item created',
    updated: 'Catalog item updated',
    archived: 'Catalog item archived'
  },
  errors: {
    load: 'Unable to load catalog items.',
    save: 'Unable to save catalog item.',
    archive: 'Unable to archive catalog item.'
  }
}
