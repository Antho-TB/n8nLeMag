import json

with open('c:\\Users\\abezille\\dev\\n8n\\lemag_webhook.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 1. Update the Prompt
new_prompt = """// On lit l'article qui arrive du nœud Loop
const item = $input.item.json;

// On construit un prompt détaillé pour Gemini
const promptText = `**Rôle et Contexte :**
Tu es un journaliste interne pour la newsletter "Le Mag'" de l'entreprise TB Groupe.
Ton style est engageant, positif, professionnel et décontracté. 
Règle absolue : Reste fidèle aux faits fournis. Aucune exagération, aucune invention, aucune extrapolation.

**Mission :**
Prends les informations brutes ci-dessous et rédige un court article (150 à 300 mots maximum) pour la newsletter.

**Données brutes de l'auteur :**
- Nom de l'auteur : ${item.name || 'Non fourni'}
- Service de l'auteur : ${item.service || 'Non fourni'}
- Titre de base proposé : ${item.Titre || 'Non fourni'}
- Contenu brut proposé : ${item.message || 'Non fourni'}

**Instructions de rédaction :**
1. **Titre :** Tu dois OBLIGATOIREMENT proposer un nouveau titre plus accrocheur et professionnel, basé sur le titre proposé.
2. **Contenu :** Améliore la fluidité et l'impact du texte tout en gardant l'idée originale intacte. Si le contenu brut est déjà excellent, limite tes modifications au strict minimum.
3. **Liens (Important) :** Si des liens URL sont présents dans le contenu brut, tu dois ABSOLUMENT les conserver intacts dans ton texte final. Ne les modifie pas.
4. **Style :** Mets en valeur l'initiative du service. Rends le contenu accessible à tous les employés. Ajoute jusqu'à 2 émojis pertinents (mais n'utilise JAMAIS l'émoji 🚀).
5. **Typographie :** Mets des majuscules uniquement aux noms propres et en début de phrase.

**Règle Anti-Hallucination CRITIQUE :**
Si le "Contenu brut proposé" est vide, "Non fourni" ou s'il ne contient aucune information concrète, tu NE DOIS PAS inventer un article. Tu dois absolument retourner le titre "Erreur de contenu" et un message demandant de fournir du contenu.

**Format de réponse EXIGÉ :**
Tu dois répondre UNIQUEMENT avec un objet JSON valide, sans balises markdown de code autour, en respectant cette structure :
{
  "title": "Le nouveau titre accrocheur",
  "content": "Le texte final de l'article avec le formatage HTML de base si nécessaire (<br>, <strong>...)"
}`;

// On retourne UNIQUEMENT le prompt
return {
  prompt: promptText,
  originalData: item 
};"""

# 2. Update the Formatage Elementor node
new_formatage = """// Elementor Webhook envoie souvent les données dans la racine ou dans "body"
const payload = $input.item.json.body || $input.item.json;

function extract(keys) {
  // If parsed as nested object
  if (payload.fields && typeof payload.fields === 'object') {
    for (const k of keys) {
      if (payload.fields[k] !== undefined) {
         let val = payload.fields[k].value || payload.fields[k].raw_value || '';
         if (val === 'empty') return '';
         return val;
      }
    }
    // Search by title
    for (const field of Object.values(payload.fields)) {
      if (keys.some(k => field.title && field.title.toLowerCase().includes(k))) {
         let val = field.value || field.raw_value || '';
         if (val === 'empty') return '';
         return val;
      }
    }
  }
  
  // If flat keys like "fields[message][value]"
  for (const k of keys) {
    const valueKey = `fields[${k}][value]`;
    if (payload[valueKey] !== undefined) {
      let val = payload[valueKey];
      if (val === 'empty') return '';
      return val;
    }
  }

  // Fallback for regular flat
  for (const k of keys) {
    if (payload[k] !== undefined) {
      let val = payload[k];
      if (val === 'empty') return '';
      return val;
    }
  }
  return '';
}

let skipAi = extract(['skip_ai', 'field_c3233c5']);
if (Array.isArray(skipAi)) skipAi = skipAi.join(',');

return {
  json: {
    submission_id: payload.form_id || payload.id || Math.random().toString(36).substr(2, 9),
    name: extract(['name', 'nom', 'auteur']) || 'Non fourni',
    service: extract(['service', 'departement', 'département', 'informatique']) || 'Non fourni',
    message: extract(['message', 'contenu', 'texte', 'actu', 'performance', 'ETL']) || '',
    Titre: extract(['titre', 'title', 'sujet', 'field_cd2aae5']) || 'Titre par défaut',
    fichier: extract(['fichier', 'file', 'image', 'photo', 'field_a70b45a']) || '',
    Categorie: extract(['categorie', 'category', 'tech']) || '',
    skip_ai: skipAi ? String(skipAi) : '',
    user_ip: payload.meta?.user_ip || 'IP Inconnue',
    created_at: new Date().toISOString()
  }
};"""

# 3. Update the Image Generation Prompt
new_image_prompt = """const item = $input.item.json;

// --- 1. Choix du Style selon la Catégorie ---
let style_keywords = "";
let style_preset = "digital-art";
const cat = (item.Categorie || item.service || "").toLowerCase();

if (cat.includes("tech") || cat.includes("informatique") || cat.includes("it")) {
    style_keywords = "style 3D isométrique, high-tech, néon subtil, épuré, représentation de données, moderne, couleurs vives avec touches de bleu et violet.";
    style_preset = "3d-model";
} else if (cat.includes("vie") || cat.includes("rh") || cat.includes("entreprise")) {
    style_keywords = "style flat design chaleureux, illustration vectorielle douce, ambiance humaine et collaborative, formes organiques, couleurs pastels et lumineuses.";
    style_preset = "flat-design";
} else if (cat.includes("produit") || cat.includes("design") || cat.includes("etude") || cat.includes("qualite") || cat.includes("méthode")) {
    style_keywords = "design industriel épuré, éclairage de studio dramatique, blueprints en arrière plan, rendu photoréaliste ou croquis détaillé de haute qualité.";
    style_preset = "photographic";
} else if (cat.includes("logistique") || cat.includes("expedition") || cat.includes("achat") || cat.includes("adv")) {
    style_keywords = "style vector-art dynamique, illustration conceptuelle sur le mouvement et les flux, symétrique, couleurs contrastées (noir, rouge, gris).";
    style_preset = "vector-art";
} else {
    // Par défaut (Fallback)
    style_keywords = "illustration conceptuelle, moderne, épurée, aux couleurs vives et professionnelles (noir, rouge, gris, blanc prédominants).";
    style_preset = "digital-art";
}

// --- 2. Règles strictes ---
const negative_prompt = "texte, mots, lettres, chiffres, logos explicites, agressif, caricatural, stéréotypes marqués, scènes génériques, couteaux tranchants, armes.";
const company_nod = "Intègre subtilement un clin d'œil à la qualité et l'innovation industrielle (lignes précises, matériaux nobles, textures métalliques) sans montrer de produits spécifiques.";

// --- 3. Construction du Prompt Final ---
const main_prompt = `Génère une illustration pour une newsletter interne. L'image doit être visuellement explicite par rapport au sujet suivant :\nSujet : "${item.title}".\nContexte : "${(item.message || '').substring(0, 300)}".\n\nDirectives artistiques obligatoires : ${style_keywords}\n${company_nod}\nN'ajoute absolument aucun texte ni mot sur l'image.`;

const randomString = Math.random().toString(36).substring(2, 8);
item.uniqueFilename = `generated-${item.submission_id}-${randomString}.png`;

const imageGenerationJson = {
  "prompt": main_prompt,
  "n": 1,
  "size": "1024x1024",
  "response_format": "b64_json",
  "style_preset": style_preset,
  "negative_prompt": negative_prompt
};

return {
  ...item,
  uniqueFilename: item.uniqueFilename,
  imageGenerationPrompt: imageGenerationJson
};"""

for node in data['nodes']:
    if node['name'] == 'Prompt pour LLM':
        node['parameters']['jsCode'] = new_prompt
    elif node['name'] == 'Formatage Elementor':
        node['parameters']['jsCode'] = new_formatage
    elif node['name'] == 'Prompt Génération Image':
        node['parameters']['jsCode'] = new_image_prompt

# 4. Fix missing connections
if 'connections' not in data:
    data['connections'] = {}

connections = data['connections']

if 'Traduction des ID' not in connections:
    connections['Traduction des ID'] = {'main': [[{'node': 'Si i\'auteur à ajouté un image alors', 'type': 'main', 'index': 0}]]}

if 'Webhook Elementor' not in connections:
    connections['Webhook Elementor'] = {'main': [[{'node': 'Formatage Elementor', 'type': 'main', 'index': 0}]]}

if 'Formatage Elementor' not in connections:
    connections['Formatage Elementor'] = {'main': [[{'node': 'Ne pas modifier si', 'type': 'main', 'index': 0}]]}

if 'Execute quand on clique' not in connections:
    connections['Execute quand on clique'] = {'main': [[{'node': 'Requète SQL sur BDD Wordpress', 'type': 'main', 'index': 0}]]}

if 'Requète SQL sur BDD Wordpress' not in connections:
    connections['Requète SQL sur BDD Wordpress'] = {'main': [[{'node': 'Ne pas modifier si', 'type': 'main', 'index': 0}]]}

with open('c:\\Users\\abezille\\dev\\n8n\\lemag_webhook.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Fixed")
