from migration import MigrationManager

migration_manager = MigrationManager()

# Dev
directory = "D:\\Data"


# migration_manager.migrate_to_mongo(directory=directory + "\\DEV_LIMSI_ASR", mongo_collection="dev_limsi_asr")
# migration_manager.migrate_to_mongo(directory=directory + "\\DEV_METADATA", mongo_collection="dev_metadata")
# migration_manager.migrate_shots_to_mongo(directory=directory + "\\DEV_SHOTS", mongo_collection="dev_shots")
#
# # Test
# migration_manager.migrate_to_mongo(directory=directory + "\\TEST_LIMSI_ASR", mongo_collection="test_limsi_asr")
# migration_manager.migrate_to_mongo(directory=directory + "\\TEST_METADATA", mongo_collection="test_metadata")
migration_manager.migrate_shots_to_mongo(directory=directory + "\\TEST_SHOTS", mongo_collection="test_shots")

