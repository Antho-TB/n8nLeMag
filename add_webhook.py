import json

with open('c:\\Users\\abezille\\dev\\n8n\\lemag_original.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

data['nodes'].append({
  "parameters": {
    "httpMethod": "POST",
    "path": "nouvelle-actu-mag",
    "options": {}
  },
  "id": "webhook-trigger",
  "name": "Webhook Elementor",
  "type": "n8n-nodes-base.webhook",
  "typeVersion": 1,
  "position": [-1552, 3000],
  "webhookId": "e549ae5a-7480-4a0d-a76c-9943dcd02f4a"
})

data['nodes'].append({
  "parameters": {
    "jsCode": "\n// Elementor Webhook envoie souvent les donnees dans la racine ou dans \"body\"\nconst body = $input.item.json.body || $input.item.json;\n\n// On map les champs d'Elementor vers ce qu'attend le webhook\nreturn {\n  json: {\n    submission_id: body.form_id || body.id || Math.random().toString(36).substr(2, 9),\n    name: body.name || 'Non fourni',\n    service: body.service || 'Non fourni',\n    message: body.message || '',\n    Titre: body.field_cd2aae5 || 'Titre par defaut',\n    fichier: body.field_a70b45a || '',\n    Categorie: body.categorie || body.Categorie || '',\n    skip_ai: body.field_c3233c5 ? String(body.field_c3233c5) : '',\n    user_ip: body.meta?.user_ip || 'IP Inconnue',\n    created_at: new Date().toISOString()\n  }\n};\n"
  },
  "id": "mapping-elementor",
  "name": "Formatage Elementor",
  "type": "n8n-nodes-base.code",
  "typeVersion": 2,
  "position": [-1056, 3000]
})

data['connections']['Webhook Elementor'] = {
  "main": [
    [
      {
        "node": "Formatage Elementor",
        "type": "main",
        "index": 0
      }
    ]
  ]
}

data['connections']['Formatage Elementor'] = {
  "main": [
    [
      {
        "node": "Ne pas modifier si",
        "type": "main",
        "index": 0
      }
    ]
  ]
}

with open('c:\\Users\\abezille\\dev\\n8n\\lemag_original.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Done")
