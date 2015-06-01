namespace py cse191.lang
struct GradeOutput {
    1:string grade,
    2:string debug,
}

exception RuntimeException {
    1:string msg,
}

service CodeExecutor {
    string run_code(1:string code) throws (1:RuntimeException ex),
    GradeOutput grade_code(1:string code, 2:string grader) throws (1:RuntimeException ex),
}
