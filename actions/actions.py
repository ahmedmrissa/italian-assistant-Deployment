from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import os
import requests

# Initialize Supabase configuration
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

class ActionExplainGrammar(Action):
    def name(self) -> Text:
        return "action_explain_grammar"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        grammar_point = next(tracker.get_latest_entity_values("grammar_point"), None)
        
        explanations = {
            "passato prossimo": "Il passato prossimo è un tempo verbale che esprime un'azione completata nel passato. Si forma con l'ausiliare (avere o essere) al presente + il participio passato del verbo principale.",
            "imperfetto": "L'imperfetto è un tempo verbale che esprime azioni abituali nel passato, descrizioni, stati d'animo o azioni in corso interrotte da un'altra azione.",
            "condizionale": "Il condizionale si usa per esprimere desideri, consigli, opinioni, supposizioni o azioni future rispetto al passato."
        }
        
        if grammar_point and grammar_point in explanations:
            message = explanations[grammar_point]
        else:
            message = "Posso spiegarti vari aspetti della grammatica italiana. Che cosa ti interessa in particolare?"
        
        dispatcher.utter_message(text=message)
        return []

class ActionTeachVocabulary(Action):
    def name(self) -> Text:
        return "action_teach_vocabulary"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        vocabulary_word = next(tracker.get_latest_entity_values("vocabulary_word"), None)
        
        vocabulary_sets = {
            "cibo": ["pizza", "pasta", "gelato", "caffè", "vino", "pane", "acqua"],
            "colori": ["rosso", "blu", "verde", "giallo", "nero", "bianco", "viola"],
            "numeri": ["uno", "due", "tre", "quattro", "cinque", "sei", "sette", "otto", "nove", "dieci"]
        }
        
        if vocabulary_word and vocabulary_word in vocabulary_sets:
            words = ", ".join(vocabulary_sets[vocabulary_word])
            message = f"Ecco alcune parole relative a {vocabulary_word}: {words}"
        else:
            message = "Posso insegnarti diverse categorie di vocaboli. Quale ti interessa?"
        
        dispatcher.utter_message(text=message)
        return []

class ActionStartConversation(Action):
    def name(self) -> Text:
        return "action_start_conversation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        topic = next(tracker.get_latest_entity_values("topic"), None)
        
        if topic:
            message = f"Ottimo! Parliamo di {topic}. Di cosa in particolare?"
        else:
            message = "Di cosa vorresti parlare?"
        
        dispatcher.utter_message(text=message)
        return []

class ActionChangeTopic(Action):
    def name(self) -> Text:
        return "action_change_topic"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message = "Certo, possiamo cambiare argomento. Di cosa vorresti parlare?"
        dispatcher.utter_message(text=message)
        return []

class ActionSetUserLevel(Action):
    def name(self) -> Text:
        return "action_set_user_level"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        level = next(tracker.get_latest_entity_values("level"), None)
        
        if level:
            message = f"Ho impostato il tuo livello a {level}."
        else:
            message = "Per favore, indicami il tuo livello di italiano (A1, A2, B1, B2, C1, C2)."
        
        dispatcher.utter_message(text=message)
        return [SlotSet("user_level", level)]

class ActionShowProgress(Action):
    def name(self) -> Text:
        return "action_show_progress"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_level = tracker.get_slot("user_level")
        
        if user_level:
            message = f"Il tuo livello attuale è {user_level}. Continua così!"
        else:
            message = "Non ho ancora informazioni sul tuo livello. Vuoi impostare il tuo livello?"
        
        dispatcher.utter_message(text=message)
        return []

class ActionProvideExercise(Action):
    def name(self) -> Text:
        return "action_provide_exercise"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message = "Ecco un esercizio per te: Completa la frase - 'Io ___ (andare) al cinema ieri.' Quale verbo usi?"
        dispatcher.utter_message(text=message)
        return []

class ActionEvaluateExercise(Action):
    def name(self) -> Text:
        return "action_evaluate_exercise"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message = "Perfetto! Hai completato l'esercizio. Vediamo i risultati."
        dispatcher.utter_message(text=message)
        return []

class ActionProvidePronunciationExercise(Action):
    def name(self) -> Text:
        return "action_provide_pronunciation_exercise"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message = "Per favore, prova a pronunciare la parola 'ciao'. Usa il pulsante di registrazione qui sotto."
        dispatcher.utter_message(text=message)
        return []

class ActionEvaluatePronunciation(Action):
    def name(self) -> Text:
        return "action_evaluate_pronunciation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message = "La tua pronuncia è molto buona! Continua a praticare."
        dispatcher.utter_message(text=message)
        return []

class ActionShareCulturalInfo(Action):
    def name(self) -> Text:
        return "action_share_cultural_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        topic = next(tracker.get_latest_entity_values("topic"), None)
        
        cultural_info = {
            "tradizioni": "L'Italia è famoria come il Carnevale di Venezia, la Festa della Repubblica il 2 giugno, e le tradizioni natalizie come i presepi.",
            "cibo": "La cucina italiana varia da regione a regione. Ad esempio, in Emilia-Romagna si mangia molto lasagne e tortellini, mentre in Sicilia si preferiscono i piatti con pesce."
        }
        
        if topic and topic in cultural_info:
            message = cultural_info[topic]
        else:
            message = "Posso raccontarti molte cose sulla cultura italiana. Cosa ti interessa di più?"
        
        dispatcher.utter_message(text=message)
        return []

class ActionAskName(Action):
    def name(self) -> Text:
        return "action_ask_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        message = "Piacere di conoscerti. Come ti chiami?"
        dispatcher.utter_message(text=message)
        return []

class ActionLogin(Action):
    def name(self) -> Text:
        return "action_login"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # In a real implementation, this would handle the login process
        # For now, we'll just simulate a successful login
        message = "Accesso effettuato con successo! Benvenuto."
        dispatcher.utter_message(text=message)
        return []

class ActionRegister(Action):
    def name(self) -> Text:
        return "action_register"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # In a real implementation, this would handle the registration process
        # For now, we'll just simulate a successful registration
        message = "Registrazione completata con successo! Benvenuto."
        dispatcher.utter_message(text=message)
        return []

class ActionLogout(Action):
    def name(self) -> Text:
        return "action_logout"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # In a real implementation, this would handle the logout process
        # For now, we'll just simulate a successful logout
        message = "Disconnessione effettuata con successo. A presto!"
        dispatcher.utter_message(text=message)
        return []

# Simple Supabase Integration Actions
class ActionSupabaseLogin(Action):
    def name(self) -> Text:
        return "action_supabase_login"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get user credentials from slots or entities
        email = next(tracker.get_latest_entity_values("email"), None)
        password = next(tracker.get_latest_entity_values("password"), None)
        
        if not email or not password:
            message = "Per favore, fornisci email e password per accedere."
            dispatcher.utter_message(text=message)
            return []
        
        try:
            # Attempt to sign in with Supabase using REST API
            if supabase_url and supabase_key:
                response = requests.post(
                    f"{supabase_url}/auth/v1/token?grant_type=password",
                    headers={
                        "apikey": supabase_key,
                        "Authorization": f"Bearer {supabase_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "email": email,
                        "password": password
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    message = "Accesso effettuato con successo! Benvenuto."
                    # Store user session data in slots if needed
                    return [SlotSet("user_id", data.get("user", {}).get("id"))]
                else:
                    message = "Credenziali non valide. Riprova."
            else:
                message = "Servizio di autenticazione non disponibile al momento."
        except Exception as e:
            message = "Errore durante l'accesso. Riprova più tardi."
            print(f"Supabase login error: {e}")
        
        dispatcher.utter_message(text=message)
        return []

class ActionSupabaseRegister(Action):
    def name(self) -> Text:
        return "action_supabase_register"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get user registration data
        email = next(tracker.get_latest_entity_values("email"), None)
        password = next(tracker.get_latest_entity_values("password"), None)
        full_name = next(tracker.get_latest_entity_values("name"), None)
        
        if not email or not password or not full_name:
            message = "Per registrarti, ho bisogno di email, password e nome completo."
            dispatcher.utter_message(text=message)
            return []
        
        try:
            # Attempt to register with Supabase using REST API
            if supabase_url and supabase_key:
                response = requests.post(
                    f"{supabase_url}/auth/v1/signup",
                    headers={
                        "apikey": supabase_key,
                        "Authorization": f"Bearer {supabase_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "email": email,
                        "password": password,
                        "data": {
                            "full_name": full_name
                        }
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    message = f"Registrazione completata con successo, {full_name}! Benvenuto."
                    return [SlotSet("user_id", data.get("user", {}).get("id"))]
                else:
                    message = "Errore durante la registrazione. Riprova."
            else:
                message = "Servizio di registrazione non disponibile al momento."
        except Exception as e:
            message = "Errore durante la registrazione. Riprova più tardi."
            print(f"Supabase registration error: {e}")
        
        dispatcher.utter_message(text=message)
        return []

class ActionSaveProgress(Action):
    def name(self) -> Text:
        return "action_save_progress"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_id = tracker.get_slot("user_id")
        user_level = tracker.get_slot("user_level")
        
        if not user_id:
            message = "Devi effettuare l'accesso per salvare i progressi."
            dispatcher.utter_message(text=message)
            return []
        
        try:
            # Save progress to Supabase using REST API
            if supabase_url and supabase_key:
                # Get current progress data
                progress_data = {
                    "user_id": user_id,
                    "skill_area": "italian",
                    "level": user_level,
                    "correct_answers": 10,  # This would be dynamic in a real implementation
                    "total_attempts": 15    # This would be dynamic in a real implementation
                }
                
                # Insert or update progress
                response = requests.post(
                    f"{supabase_url}/rest/v1/progress",
                    headers={
                        "apikey": supabase_key,
                        "Authorization": f"Bearer {supabase_key}",
                        "Content-Type": "application/json",
                        "Prefer": "return=representation"
                    },
                    json=progress_data
                )
                
                if response.status_code == 201:
                    message = "Progressi salvati con successo!"
                else:
                    message = "Errore durante il salvataggio dei progressi."
            else:
                message = "Servizio di salvataggio non disponibile al momento."
        except Exception as e:
            message = "Errore durante il salvataggio dei progressi."
            print(f"Supabase save progress error: {e}")
        
        dispatcher.utter_message(text=message)
        return []

class ActionLoadProgress(Action):
    def name(self) -> Text:
        return "action_load_progress"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_id = tracker.get_slot("user_id")
        
        if not user_id:
            message = "Devi effettuare l'accesso per caricare i progressi."
            dispatcher.utter_message(text=message)
            return []
        
        try:
            # Load progress from Supabase using REST API
            if supabase_url and supabase_key:
                response = requests.get(
                    f"{supabase_url}/rest/v1/progress?user_id=eq.{user_id}",
                    headers={
                        "apikey": supabase_key,
                        "Authorization": f"Bearer {supabase_key}"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data:
                        # Get the most recent progress entry
                        progress_data = data[-1]  # Assuming the last entry is the most recent
                        level = progress_data.get("level", "A1")
                        message = f"Il tuo livello attuale è {level}. Continua così!"
                        return [SlotSet("user_level", level)]
                    else:
                        message = "Nessun dato di progresso trovato."
                else:
                    message = "Errore durante il caricamento dei progressi."
            else:
                message = "Servizio di caricamento non disponibile al momento."
        except Exception as e:
            message = "Errore durante il caricamento dei progressi."
            print(f"Supabase load progress error: {e}")
        
        dispatcher.utter_message(text=message)
        return []

class ActionSaveConversation(Action):
    def name(self) -> Text:
        return "action_save_conversation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_id = tracker.get_slot("user_id")
        
        if not user_id:
            message = "Devi effettuare l'accesso per salvare la cronologia delle conversazioni."
            dispatcher.utter_message(text=message)
            return []
        
        try:
            # Save conversation to Supabase using REST API
            if supabase_url and supabase_key:
                # Get conversation data
                conversation_data = {
                    "user_id": user_id,
                    "started_at": "NOW()",  # This would be dynamic in a real implementation
                    "ended_at": "NOW()",    # This would be dynamic in a real implementation
                    "difficulty_level": tracker.get_slot("user_level") or "A1",
                    "topics_discussed": ["italian"]  # This would be dynamic in a real implementation
                }
                
                # Insert conversation
                response = requests.post(
                    f"{supabase_url}/rest/v1/conversations",
                    headers={
                        "apikey": supabase_key,
                        "Authorization": f"Bearer {supabase_key}",
                        "Content-Type": "application/json",
                        "Prefer": "return=representation"
                    },
                    json=conversation_data
                )
                
                if response.status_code == 201:
                    message = "Cronologia delle conversazioni salvata con successo!"
                else:
                    message = "Errore durante il salvataggio della cronologia delle conversazioni."
            else:
                message = "Servizio di salvataggio non disponibile al momento."
        except Exception as e:
            message = "Errore durante il salvataggio della cronologia delle conversazioni."
            print(f"Supabase save conversation error: {e}")
        
        dispatcher.utter_message(text=message)
        return []