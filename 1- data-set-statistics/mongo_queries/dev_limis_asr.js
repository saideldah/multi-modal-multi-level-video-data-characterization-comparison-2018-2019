// db.getCollection("dev_limsi_asr").find().limit(1)
// db.getCollection("dev_limsi_asr").count()

// db.getCollection("dev_limsi_asr").count({ "AudioDoc.SpeakerList.Speaker": { $exists: true , $ne: []} })

// db.getCollection("dev_limsi_asr").count({ "AudioDoc.SpeakerList": { $exists: true, $eq: null } })

// avaerage number of speakers
//db.getCollection("dev_limsi_asr").aggregate([
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

//db.getCollection("dev_limsi_asr").aggregate([
// //    {
// //        $group: {
// //            _id: null,
// //            "total_segments": {
// //                $sum: {
// //                    $cond: {
// //                        if: { $isArray: "$AudioDoc.SegmentList.SpeechSegment" },
// //                        then: { $size: "$AudioDoc.SegmentList.SpeechSegment" },
// //                        else: 1
// //                    }
// //                }
// //            }
// //        }
// //    }
// //])


var group = [
    {
        $group: {
            _id: null,
            "max-segments-per-video": {
                $max: {
                    $cond: {
                        if: {$isArray: "$AudioDoc.SegmentList.SpeechSegment"},
                        then: {$size: "$AudioDoc.SegmentList.SpeechSegment"},
                        else: 1
                    }
                }
            }
        }
    }
]
var group = [
    {
        $group: {
            _id: null,
            "min-segments-per-video": {
                $min: {
                    $cond: {
                        if: {$isArray: "$AudioDoc.SegmentList.SpeechSegment"},
                        then: {$size: "$AudioDoc.SegmentList.SpeechSegment"},
                        else: 1
                    }
                }
            }
        }
    }
]

db.dev_limsi_asr.aggregate(group)


var query = {
    "AudioDoc.SegmentList.SpeechSegment":
        {
            $exists: true,
            $ne: []
        }
}
db.dev_limsi_asr.count() - db.dev_limsi_asr.count(query)


function compare() {
    return this.end - this.start > 1
}

var query = {$where: compare}

db.dev_limsi_asr.count(query)


db.test.aggregate([
    {
        $unwind: "$segments"
    },
    {
        $group: {
            _id: null,
            segments: {$push: "$segments"}
        }
    },
    {
        $project: {
            _id: 0
        }
    }
])


//-------------------------

//
//var data = [
//    {
//        segments: [
//            {
//                start: 0.9,
//                end: 1
//
//            }
//            ,{
//                start: 2,
//                end: 5
//
//            }
//            ,{
//                start: 6,
//                end: 6.9
//
//            }
//            ,{
//                start: 8,
//                end: 10
//
//            }
//            ,{
//                start: 11,
//                end: 20
//
//            }
//        ]
//    }
//    ,{
//        segments: [
//            {
//                start: 2,
//                end: 3
//
//            },
//            {
//                start:5,
//                end: 6
//
//            },
//            {
//                start: 9,
//                end: 10
//
//            },
//            {
//                start: 20,
//                end: 30
//
//            },
//            {
//                start: 33,
//                end: 33.5
//
//            },
//        ]
//    }
//    ,{
//        segments: [
//            {
//                start: 20,
//                end: 30
//
//            }
//        ]
//    }
//    ,{
//        segments: [
//            {
//                start: 33,
//                end: 33.5
//
//            }
//        ]
//    }
//    ,{
//        segments: null
//    }
//]
//db.test.insertMany(data)
//

db.test.aggregate([
    {
        $unwind: "$segments"
    },
    {
        $project: {
            _id: 0,
            duration: {$subtract: ["$segments.end", "$segments.start"]},
            start: "$segments.start",
            end: "$segments.end",
        }
    },
    {
        $match: {
            "duration": {$gt: 1}
        }
    },
    {
        $group:
            {
                _id: 0,
                minDuration: {$min: "$duration"}
            }
    }
])

////////////////-
//min

db.dev_limsi_asr.aggregate([
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
            duration: { $subtract: [{$toDouble: "$speechSegmentList.@etime"}, {$toDouble: "$speechSegmentList.@stime"}] },
            start: "$speechSegmentList.@stime",
            end: "$speechSegmentList.@etime",
        }
    },
    {
        $match: {
            "duration": { $gt: 2 }
        }
    },
    {
        $group:
            {
                _id: 0,
                minDuration: { $min: "$duration" }
            }
    }
])
//////////////////-
//MAX segment duration


db.dev_limsi_asr.aggregate([
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
            duration: { $subtract: [{$toDouble: "$speechSegmentList.@etime"}, {$toDouble: "$speechSegmentList.@stime"}] },
            start: "$speechSegmentList.@stime",
            end: "$speechSegmentList.@etime",
        }
    },
    {
        $match: {
            "duration": { $gt: 2 }
        }
    },
    {
        $group:
            {
                _id: 0,
                maxDuration: { $max: "$duration" }
            }
    }
])

//---------------------------------------
//max words
db.dev_limsi_asr.aggregate([
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
            wordsCount: {
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
            "duration": { $gt: 2 }
        }
    },
    {
        $group:
            {
                _id: 0,
                maxWordsCount: { $max: "$wordsCount" }
            }
    }
])

////---------------------------------------------------------
//Max Words Per Speech Segment

db.dev_limsi_asr.aggregate([
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
            words: "$speechSegmentList.Word"
        }
    },
    {
        $match: {
            "duration": { $gt: 2 }
        }
    },
    {
        $group:
            {
                _id: 0,
                maxWordPerSegment: {
                    $max: {
                        $cond: {
                            if: { $isArray: "$words" },
                            then: { $size: "$words" },
                            else: 1
                        }
                    }
                }
            }
    }
])      

//////////////////--------------------------------------
//Min Words
db.dev_limsi_asr.aggregate([
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
                minWordPerSegment: { $min: "$numberOfWords" }
            }
    }
])                               