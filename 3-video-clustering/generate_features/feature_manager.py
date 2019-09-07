import xml.dom.minidom


class FeatureManager:
    def __init__(self, directory_path, file_name):
        self.__file_name = file_name
        self.__file_path = directory_path + file_name

    @staticmethod
    def __get_interactions(shot):
        interactions_list = []
        interactions = shot.getElementsByTagName("Interaction")
        for interaction in interactions:
            interactions_list.append(float(interaction.childNodes[0].data))
        return interactions_list

    @staticmethod
    def __get_interventions(shot):
        intervention_list = []
        interventions = shot.getElementsByTagName("Intervention")
        for intervention in interventions:
            intervention_list.append(float(intervention.childNodes[0].data))
        return intervention_list

    @staticmethod
    def __get_speaker_types(shot):
        speaker_types_list = []

        ponctuel = shot.getElementsByTagName("Ponctuel")
        localise = shot.getElementsByTagName("Localise")
        present = shot.getElementsByTagName("Present")
        regulier = shot.getElementsByTagName("Regulier")
        important = shot.getElementsByTagName("Important")

        speaker_types_list.append(float(ponctuel[0].firstChild.nodeValue))
        speaker_types_list.append(float(localise[0].firstChild.nodeValue))
        speaker_types_list.append(float(present[0].firstChild.nodeValue))
        speaker_types_list.append(float(regulier[0].firstChild.nodeValue))
        speaker_types_list.append(float(important[0].firstChild.nodeValue))

        return speaker_types_list

    @staticmethod
    def __get_speaker_distributions(shot):
        speaker_distribution_list = []
        speaker_distributions = shot.getElementsByTagName("SpeakerDistribution")
        for speaker_distribution in speaker_distributions:
            speaker_distribution_list.append(float(speaker_distribution.childNodes[0].data))
        return speaker_distribution_list

    @staticmethod
    def __get_number_of_faces(shot):
        number_of_face_list = []
        mean_nb_faces = shot.getElementsByTagName("MeanNbFaces")
        std_nb_faces = shot.getElementsByTagName("StdNbFaces")
        number_of_face_list.append(float(mean_nb_faces[0].firstChild.nodeValue))
        number_of_face_list.append(float(std_nb_faces[0].firstChild.nodeValue))
        return number_of_face_list

    @staticmethod
    def __get_intensity_variation_list(shot):
        intensity_variation_list = []
        inter_intensity_variations = shot.getElementsByTagName("InterIntensityVariation")
        intra_intensity_variations = shot.getElementsByTagName("IntraIntensityVariation")

        for inter_intensity_variation in inter_intensity_variations:
            intensity_variation_list.append(float(inter_intensity_variation.firstChild.nodeValue))

        for intra_intensity_variation in intra_intensity_variations:
            intensity_variation_list.append(float(intra_intensity_variation.firstChild.nodeValue))
        return intensity_variation_list

    @staticmethod
    def __get_number_shot_transition(shot):
        number_shot_transition_list = []
        number_shot_transition = shot.getElementsByTagName("NumberShotTransition")
        number_shot_transition_list.append(float(number_shot_transition[0].firstChild.nodeValue))

        return number_shot_transition_list

    @staticmethod
    def __get_number_speaker_transition(shot):
        number_speaker_transition_list = []
        number_speaker_transition = shot.getElementsByTagName("NumberSpeakerTransition")
        number_speaker_transition_list.append(float(number_speaker_transition[0].firstChild.nodeValue))

        return number_speaker_transition_list

    @staticmethod
    def __get_speech_music_alignment(shot):
        speech_music_alignment_list = []
        speech = shot.getElementsByTagName("Speech")
        music = shot.getElementsByTagName("Music")
        speech_with_music = shot.getElementsByTagName("SpeechWithMusic")
        speech_with_non_music = shot.getElementsByTagName("SpeechWithNonMusic")
        non_speech_with_music = shot.getElementsByTagName("NonSpeechWithMusic")
        non_speech_with_non_music = shot.getElementsByTagName("NonSpeechWithNonMusic")

        speech_music_alignment_list.append(float(speech[0].firstChild.nodeValue))
        speech_music_alignment_list.append(float(music[0].firstChild.nodeValue))
        speech_music_alignment_list.append(float(speech_with_music[0].firstChild.nodeValue))
        speech_music_alignment_list.append(float(speech_with_non_music[0].firstChild.nodeValue))
        speech_music_alignment_list.append(float(non_speech_with_music[0].firstChild.nodeValue))
        speech_music_alignment_list.append(float(non_speech_with_non_music[0].firstChild.nodeValue))

        return speech_music_alignment_list

    @staticmethod
    def __get_number_of_words(shot):
        number_of_words = shot.getElementsByTagName("Words")
        length = number_of_words[0].getAttribute('length_percentage')
        return float(length)

    @staticmethod
    def __get_duration(shot):
        duration = shot.getAttribute("duration_percentage")
        return float(duration)

    @staticmethod
    def __get_category(shot):
        category = shot.getAttribute("category")
        return category

    def get_feature_vector_list(self):
        # print self.__file_path
        input_dom_tree = xml.dom.minidom.parse(self.__file_path)
        shots = input_dom_tree.getElementsByTagName("Shot")
        shot_feature_vector_list = []
        shot_number = 1
        for shot in shots:
            vector = [self.__file_name, shot_number]
            category = self.__get_category(shot)
            vector.append(category)
            interactions = self.__get_interactions(shot)

            interventions = self.__get_interventions(shot)

            speaker_types = self.__get_speaker_types(shot)

            speaker_distributions = self.__get_speaker_distributions(shot)

            number_of_faces = self.__get_number_of_faces(shot)

            inter_intensity_variation_list = self.__get_intensity_variation_list(shot)

            number_shot_transition_list = self.__get_number_shot_transition(shot)

            number_speaker_transition_list = self.__get_number_speaker_transition(shot)

            speech_music_alignment_list = self.__get_speech_music_alignment(shot)

            vector = vector + interactions + interventions + speaker_types + speaker_distributions + number_of_faces \
                     + inter_intensity_variation_list + number_shot_transition_list + number_speaker_transition_list \
                     + speech_music_alignment_list

            number_of_words = self.__get_number_of_words(shot)

            duration = self.__get_duration(shot)

            vector.append(number_of_words)

            vector.append(duration)

            shot_feature_vector_list.append(vector)
            shot_number += 1

        return shot_feature_vector_list
