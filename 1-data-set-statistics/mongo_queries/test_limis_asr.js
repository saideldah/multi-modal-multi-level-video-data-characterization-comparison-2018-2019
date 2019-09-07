// db.getCollection("test_limsi_asr").find().limit(1)
// db.getCollection("test_limsi_asr").count()

// db.getCollection("test_limsi_asr").count({ "AudioDoc.SpeakerList.Speaker": { $exists: true , $ne: []} })

// db.getCollection("test_limsi_asr").count({ "AudioDoc.SpeakerList": { $exists: true, $eq: null } })

// avaerage number of speakers 
//db.getCollection("test_limsi_asr").aggregate([
//    {
//        $group: {
//            _id: null,
//            "total_segments": {
//                $sum: {
//                    $cond: {
//                        if: { $isArray: "$AudioDoc.SpeakerList.Speaker" },
//                        then: { $size: "$AudioDoc.SpeakerList.Speaker" },
//                        else: 1
//                    }
//                }
//            }
//        }
//    }
//])
// avearage number of speach segments

db.getCollection("test_limsi_asr").aggregate([
    {
        $group: {
            _id: null,
            "total_segments": {
                $sum: {
                    $cond: {
                        if: { $isArray: "$AudioDoc.SegmentList.SpeechSegment" },
                        then: { $size: "$AudioDoc.SegmentList.SpeechSegment" },
                        else: 1
                    }
                }
            }
        }
    }
])
///////////////////----------------------
// Max Words per Segment

db.test_limsi_asr.aggregate([
    {
        $project: {
            "speechSegmentList": "$AudioDoc.SegmentList.SpeechSegment"
        }
    },
    {
        $match:
            {
                "speechSegmentList": { $exists: true }
            }
    },
    {
        $unwind: "$speechSegmentList"
    },
    {
        $project: {
            _id: 0,
            duration: { $subtract: [{ $toDouble: "$speechSegmentList.@etime" }, { $toDouble: "$speechSegmentList.@stime" }] },
            start: "$speechSegmentList.@stime",
            end: "$speechSegmentList.@etime",
            numberOfWords: {
                $cond: {
                    if: { $isArray: "$speechSegmentList.Word" },
                    then: { $size: "$speechSegmentList.Word" },
                    else: 1
                }
            },
            words: "$speechSegmentList.Word"
        }
    },
    {
        $match: {
            $and: [
                {
                    "numberOfWords": { $gt: 3 }
                },
                {
                    "duration": { $gt: 3 }
                }
            ]

        }
    },
    {
        $group:
            {
                _id: 0,
                maxWordPerSegment: { $max: "$numberOfWords" }
            }
    }
])                               