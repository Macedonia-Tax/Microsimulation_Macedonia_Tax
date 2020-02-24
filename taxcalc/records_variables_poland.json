{
  "read": {
    "id": {
      "required": true,
      "type": "int",
      "desc": "Unique positive numeric identifier for filing unit",
      "form": {"2017": "private info"}
    },
    "legal_eng": {
      "required": true,
      "type": "string",
      "desc": "Legal Form of the business in English",
      "form": {"2017": "Field no. 3 in form CIT-8"}
    },
    "tax_basis_before_deductions": {
      "required": true,
      "type": "float",
      "desc": "Income tax base before deductions",
      "form": {"2017": "CIT-8 field no. 108"}
    },
    "deductions_from_tax_base": {
      "required": true,
      "type": "float",
      "desc": "Total deductions from taxable amount",
      "form": {"2017": "CIT-8 field no. 112"}
    }
  },
  "calc": {
    "income_tax_base_after_deductions": {
      "type": "float",
      "desc": "Income tax base",
      "form": {"2017": "CIT-8 field no. 119"}
    },
    "citax": {
      "type": "float",
      "desc": "CIT liability",
      "form": {"2017": "CIT-8 field no. 126"}
    }
  }
}
